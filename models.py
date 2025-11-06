from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid


class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    EXPIRED = "expired"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    SETTLEMENT = "settlement"
    CANCEL = "cancel"
    DENY = "deny"
    EXPIRE = "expire"


class ProductType(str, Enum):
    EBOOK = "ebook"
    MINIGAME = "minigame"
    EBOOK_EXCLUSIVE = "ebook_exclusive"


class EbookPage(BaseModel):
    page: int
    color: str
    imageUrl: Optional[str] = None


class Ebook(BaseModel):
    id: int
    title: str
    category: str
    ageGroup: str
    ageLabel: str
    description: str
    price: int
    fileName: Optional[str] = None  # Optional for mini-games
    coverColor: Optional[str] = None  # Optional for mini-games
    pages: Optional[List[EbookPage]] = []
    isBonus: Optional[bool] = False
    driveDownloadLink: Optional[str] = None  # Google Drive direct download link
    productType: str = "ebook"  # Product type identifier
    # Mini-game specific fields
    thumbnailUrl: Optional[str] = None
    gameUrl: Optional[str] = None
    icon: Optional[str] = None


class MiniGame(BaseModel):
    id: int
    title: str
    description: str
    ageGroup: str
    ageLabel: str
    price: int  # Price per day
    thumbnailUrl: Optional[str] = None
    gameUrl: str  # URL to the game page
    category: str = "Mini Game"
    productType: str = "minigame"
    accessDuration: int = 24  # Hours of access


class EbookExclusive(BaseModel):
    id: int
    title: str
    category: str
    ageGroup: str
    ageLabel: str
    description: str
    price: int
    fileName: str
    coverColor: str
    pages: Optional[List[EbookPage]] = []
    driveDownloadLink: Optional[str] = None
    hasAudio: bool = True  # Text-to-speech feature
    hasInteractive: bool = True  # Interactive elements
    productType: str = "ebook_exclusive"


class GameAccessToken(BaseModel):
    tokenId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    gameId: int
    customerEmail: str
    customerName: str
    orderId: str
    gameUrl: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    expiresAt: datetime  # 24 hours from creation
    isActive: bool = True
    accessCount: int = 0  # Track how many times accessed


class OrderItem(BaseModel):
    productId: int  # Can be ebookId, gameId, or exclusiveId
    productType: ProductType
    title: str
    quantity: int
    price: int
    driveDownloadLink: Optional[str] = None  # For ebooks and exclusive
    gameUrl: Optional[str] = None  # For mini games
    accessToken: Optional[str] = None  # For mini games


class OrderItemCreate(BaseModel):
    productId: int
    productType: ProductType
    quantity: int = 1


class OrderCreate(BaseModel):
    customerEmail: EmailStr
    customerName: str
    customerPhone: Optional[str] = ""  # Optional WhatsApp phone number
    items: List[OrderItemCreate]


class Order(BaseModel):
    orderId: str
    customerEmail: str
    customerName: str
    customerPhone: Optional[str] = ""  # Optional WhatsApp phone number
    items: List[OrderItem]
    subtotal: int
    discount: int
    total: int
    bundleApplied: bool
    paymentStatus: PaymentStatus
    midtransOrderId: Optional[str] = None
    midtransTransactionId: Optional[str] = None
    snapToken: Optional[str] = None
    notionDownloadLink: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    paidAt: Optional[datetime] = None


class OrderResponse(BaseModel):
    orderId: str
    snapToken: str
    total: int
    redirectUrl: str


class PaymentVerification(BaseModel):
    orderId: str
    transactionStatus: str


class Payment(BaseModel):
    orderId: str
    midtransTransactionId: str
    transactionStatus: TransactionStatus
    paymentType: str
    grossAmount: int
    transactionTime: datetime
    fraudStatus: Optional[str] = None
    webhookData: dict = {}
    createdAt: datetime = Field(default_factory=datetime.utcnow)
