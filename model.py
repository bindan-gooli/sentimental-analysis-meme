import os
os.environ["USE_TF"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
import torch.nn as nn
from transformers import AutoModel
import torchvision.models as models

class IndicSentM(nn.Module):
    """
    IndicSent-M: Multimodal Sentiment Analysis Network.
    Combines BERT text representations and ResNet-50 visual features
    via multihead cross-modal attention.
    Classes: 0: Negative, 1: Neutral, 2: Positive
    """
    def __init__(
        self,
        text_model_name: str = "bert-base-multilingual-cased",
        num_classes: int = 3,
        embed_dim: int = 256,
        freeze_encoders: bool = True
    ):
        super().__init__()
        # 1. Multilingual BERT text encoder
        self.text_encoder = AutoModel.from_pretrained(text_model_name)
        text_dim = self.text_encoder.config.hidden_size  # 768

        # 2. ResNet-50 vision encoder
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.vision_encoder = nn.Sequential(*list(resnet.children())[:-1])
        vision_dim = resnet.fc.in_features  # 2048

        if freeze_encoders:
            for p in self.text_encoder.parameters():
                p.requires_grad = False
            for p in self.vision_encoder.parameters():
                p.requires_grad = False

        # 3. Latent space projection
        self.proj_t = nn.Sequential(
            nn.Linear(text_dim, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.GELU()
        )
        self.proj_v = nn.Sequential(
            nn.Linear(vision_dim, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.GELU()
        )

        # 4. Cross-Modal Attention (Text queries Vision context)
        self.cross_attn = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=4, batch_first=True)
        self.norm = nn.LayerNorm(embed_dim)

        # 5. Sentiment Classifier
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(embed_dim, 128),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor, pixel_values: torch.Tensor) -> torch.Tensor:
        # Extract text representation combining [CLS] and attention-masked mean pooling: [Batch, text_dim]
        text_outputs = self.text_encoder(input_ids=input_ids, attention_mask=attention_mask)
        mask = attention_mask.unsqueeze(-1).expand(text_outputs.last_hidden_state.size()).float()
        sum_embeddings = torch.sum(text_outputs.last_hidden_state * mask, dim=1)
        sum_mask = torch.clamp(mask.sum(dim=1), min=1e-9)
        mean_pooled = sum_embeddings / sum_mask
        cls_token = text_outputs.last_hidden_state[:, 0, :]
        h_t = 0.5 * cls_token + 0.5 * mean_pooled
        z_t = self.proj_t(h_t)

        # Extract pooled visual representation: [Batch, vision_dim]
        h_v = self.vision_encoder(pixel_values).squeeze(-1).squeeze(-1)
        z_v = self.proj_v(h_v)

        # Cross-modal attention: query = text, key/value = image
        q = z_t.unsqueeze(1)
        k = v = z_v.unsqueeze(1)
        attn_out, _ = self.cross_attn(query=q, key=k, value=v)
        fused = self.norm(z_t + attn_out.squeeze(1))

        return self.classifier(fused)
