import rsa
from asyncio import StreamReader, StreamWriter
from utils.config import EncryptionConfig

class EncryptionManager:
    public_key: rsa.PublicKey
    private_key: rsa.PrivateKey
    public_key_send: rsa.PublicKey
    config = EncryptionConfig()
    
    def __init__(self, key_size: int = config.rsa_key_default_size) -> None:
        self.public_key_send, self.private_key = rsa.newkeys(2048)
        self.public_key = None
        
    async def share_keys(self, reader: StreamReader, writer: StreamWriter) -> None:
        public_key_recv_raw = b""
        while not public_key_recv_raw.endswith(b"\n-----END RSA PUBLIC KEY-----\n"):
            public_key_recv_raw += await reader.read(1)
            
        writer.write(self.public_key_send.save_pkcs1())
        
        self.public_key = rsa.PublicKey.load_pkcs1(public_key_recv_raw)
        
    def encrypt(self, msg: bytes) -> bytes:
        if self.public_key:
            return rsa.encrypt(msg, self.public_key)
        return None
    
    def decrypt(self, msg: bytes) -> bytes:
        if self.private_key:
            return rsa.decrypt(msg, self.private_key)
        return None