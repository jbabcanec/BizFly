"""
Preview Server System - Dynamic website preview with graceful lifecycle management
"""
import asyncio
import os
import subprocess
import socket
import time
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import logging
import json
import signal

logger = logging.getLogger(__name__)


class PreviewServer:
    """
    Manages individual preview server instances
    Each website gets its own isolated server on a unique port
    """
    
    def __init__(self, business_id: str, port: int):
        self.business_id = business_id
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.started_at: Optional[datetime] = None
        self.last_accessed: Optional[datetime] = None
        self.website_path = Path(f"../generated_websites/{business_id}")
        self.timeout_minutes = 30  # Auto-shutdown after 30 minutes
        
    async def start(self) -> bool:
        """Start the preview server"""
        if not self.website_path.exists():
            logger.error(f"Website path not found: {self.website_path}")
            return False
        
        try:
            # Use Python's built-in HTTP server for simplicity
            cmd = [
                "python3", "-m", "http.server", 
                str(self.port),
                "--directory", str(self.website_path)
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid  # Create new process group for clean shutdown
            )
            
            self.started_at = datetime.utcnow()
            self.last_accessed = datetime.utcnow()
            
            # Wait a moment to ensure server started
            await asyncio.sleep(0.5)
            
            if self.is_running():
                logger.info(f"Preview server started for {self.business_id} on port {self.port}")
                return True
            else:
                logger.error(f"Preview server failed to start for {self.business_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting preview server: {e}")
            return False
    
    def stop(self):
        """Gracefully stop the preview server"""
        if self.process:
            try:
                # Send SIGTERM to process group
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                # Wait up to 5 seconds for graceful shutdown
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if doesn't stop gracefully
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
            except ProcessLookupError:
                # Process already dead
                pass
            
            self.process = None
            logger.info(f"Preview server stopped for {self.business_id}")
    
    def is_running(self) -> bool:
        """Check if server is still running"""
        if not self.process:
            return False
        return self.process.poll() is None
    
    def touch(self):
        """Update last accessed time"""
        self.last_accessed = datetime.utcnow()
    
    def is_expired(self) -> bool:
        """Check if server should be shut down due to inactivity"""
        if not self.last_accessed:
            return False
        
        expiry_time = self.last_accessed + timedelta(minutes=self.timeout_minutes)
        return datetime.utcnow() > expiry_time
    
    def get_info(self) -> Dict:
        """Get server information"""
        return {
            "business_id": self.business_id,
            "port": self.port,
            "url": f"http://localhost:{self.port}",
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "is_running": self.is_running(),
            "timeout_minutes": self.timeout_minutes
        }


class PreviewServerManager:
    """
    Manages all preview servers with lifecycle management
    """
    
    def __init__(self):
        self.servers: Dict[str, PreviewServer] = {}
        self.port_range = range(8001, 9000)
        self.used_ports: set = set()
        self._cleanup_task = None
        
    async def start(self):
        """Start the manager and cleanup task"""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("Preview server manager started")
    
    async def stop(self):
        """Stop all servers and cleanup"""
        if self._cleanup_task:
            self._cleanup_task.cancel()
        
        # Stop all running servers
        for server in self.servers.values():
            server.stop()
        
        self.servers.clear()
        self.used_ports.clear()
        logger.info("Preview server manager stopped")
    
    def _find_free_port(self) -> Optional[int]:
        """Find an available port in the range"""
        for port in self.port_range:
            if port not in self.used_ports:
                # Check if port is actually free
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    try:
                        s.bind(('', port))
                        return port
                    except OSError:
                        continue
        return None
    
    async def create_preview(self, business_id: str) -> Optional[Dict]:
        """Create or return existing preview server"""
        
        # Check if server already exists
        if business_id in self.servers:
            server = self.servers[business_id]
            if server.is_running():
                server.touch()
                return server.get_info()
            else:
                # Remove dead server
                self.used_ports.discard(server.port)
                del self.servers[business_id]
        
        # Find available port
        port = self._find_free_port()
        if not port:
            logger.error("No available ports for preview server")
            return None
        
        # Create and start new server
        server = PreviewServer(business_id, port)
        if await server.start():
            self.servers[business_id] = server
            self.used_ports.add(port)
            return server.get_info()
        
        return None
    
    def stop_preview(self, business_id: str) -> bool:
        """Stop a specific preview server"""
        if business_id in self.servers:
            server = self.servers[business_id]
            server.stop()
            self.used_ports.discard(server.port)
            del self.servers[business_id]
            return True
        return False
    
    def get_preview_info(self, business_id: str) -> Optional[Dict]:
        """Get information about a preview server"""
        if business_id in self.servers:
            server = self.servers[business_id]
            if server.is_running():
                server.touch()
                return server.get_info()
        return None
    
    def list_previews(self) -> List[Dict]:
        """List all active preview servers"""
        previews = []
        for server in self.servers.values():
            if server.is_running():
                previews.append(server.get_info())
        return previews
    
    async def _cleanup_loop(self):
        """Background task to clean up expired servers"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                expired = []
                for business_id, server in self.servers.items():
                    if server.is_expired() or not server.is_running():
                        expired.append(business_id)
                
                for business_id in expired:
                    logger.info(f"Cleaning up expired preview server: {business_id}")
                    self.stop_preview(business_id)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")


# Global instance
preview_manager = PreviewServerManager()


class PreviewServerAPI:
    """
    API interface for preview server management
    """
    
    @staticmethod
    async def start_preview(business_id: str) -> Dict:
        """Start a preview server for a business"""
        info = await preview_manager.create_preview(business_id)
        if info:
            return {
                "success": True,
                "preview": info
            }
        return {
            "success": False,
            "error": "Failed to start preview server"
        }
    
    @staticmethod
    def stop_preview(business_id: str) -> Dict:
        """Stop a preview server"""
        if preview_manager.stop_preview(business_id):
            return {
                "success": True,
                "message": "Preview server stopped"
            }
        return {
            "success": False,
            "error": "Preview server not found"
        }
    
    @staticmethod
    def get_preview_status(business_id: str) -> Dict:
        """Get preview server status"""
        info = preview_manager.get_preview_info(business_id)
        if info:
            return {
                "success": True,
                "preview": info
            }
        return {
            "success": False,
            "error": "Preview server not running"
        }
    
    @staticmethod
    def list_all_previews() -> Dict:
        """List all active preview servers"""
        return {
            "success": True,
            "previews": preview_manager.list_previews(),
            "count": len(preview_manager.servers)
        }


# Advanced features for production
class WebSocketLiveReload:
    """WebSocket server for live reload functionality"""
    
    def __init__(self, preview_server: PreviewServer):
        self.preview_server = preview_server
        self.clients = set()
        
    async def notify_change(self, file_path: str):
        """Notify all connected clients of file change"""
        message = json.dumps({
            "type": "reload",
            "file": file_path,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Send to all connected clients
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except:
                disconnected.add(client)
        
        # Remove disconnected clients
        self.clients -= disconnected


class FileWatcher:
    """Watch for file changes and trigger live reload"""
    
    def __init__(self, path: Path, callback):
        self.path = path
        self.callback = callback
        self.file_times = {}
        
    async def watch(self):
        """Watch for file changes"""
        while True:
            try:
                for file_path in self.path.rglob("*"):
                    if file_path.is_file():
                        mtime = file_path.stat().st_mtime
                        
                        if file_path in self.file_times:
                            if mtime > self.file_times[file_path]:
                                # File changed
                                await self.callback(str(file_path))
                        
                        self.file_times[file_path] = mtime
                
                await asyncio.sleep(1)  # Check every second
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in file watcher: {e}")