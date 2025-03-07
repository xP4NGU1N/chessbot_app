import torch
import torch.nn as nn

class GiraffeOriginal(nn.Module):
    def __init__(self, global_dim, piece_dim, square_dim, global_nodes, piece_nodes, square_nodes, fc_nodes, dropout_rate):
        super(GiraffeOriginal, self).__init__()

        self.global_fc = nn.Sequential(
            nn.Linear(global_dim, global_nodes),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        )

        self.piece_fc = nn.Sequential(
            nn.Linear(piece_dim, piece_nodes),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        )

        self.square_fc = nn.Sequential(
            nn.Linear(square_dim, square_nodes),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        )

        self.combined_fc = nn.Sequential(
            nn.Linear(global_nodes+piece_nodes+square_nodes, fc_nodes),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(fc_nodes, 1),
            nn.Tanh()
        )

    def forward(self, X_g, X_p, X_s):
        x_g = self.global_fc(X_g)
        x_p = self.piece_fc(X_p)
        x_s = self.square_fc(X_s)
        x = torch.cat((x_g, x_p, x_s), dim=1)
        return self.combined_fc(x)
    
class Pos2Vec(nn.Module):
    def __init__(self, input_size, output_size):
        super(Pos2Vec, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_size, output_size),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(output_size, input_size),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

class FinalPos2Vec(nn.Module):
    def __init__(self, layer_sizes):
        super(FinalPos2Vec, self).__init__()
        self.encoders = nn.ModuleList([
            Pos2Vec(layer_sizes[i], layer_sizes[i+1]) for i in range(len(layer_sizes)-1)
        ])

    def forward(self, x):
        for encoder in self.encoders:
            x, _ = encoder(x)
        return x

class GiraffeWithDeepChess(nn.Module):
    def __init__(self, pos2vec):
        super(GiraffeWithDeepChess, self).__init__()
        self.pos2vec = pos2vec
        for param in self.pos2vec.parameters():
            param.requires_grad = True
        self.nn_layers = nn.Sequential(
            nn.Linear(100, 32),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(32, 1),
            nn.Tanh()
        )

    def forward(self, x):
        embedded_feat = self.pos2vec(x)
        output = self.nn_layers(embedded_feat)
        return output

class GiraffeWithTransformer(nn.Module):
    def __init__(self, pos2vec, embed_dim=100, num_heads=4, ff_dim=256, num_layers=2, dropout_rate=0.5):
        super(GiraffeWithTransformer, self).__init__()
        self.dropout_rate = dropout_rate
        self.pos2vec = pos2vec
        for param in self.pos2vec.parameters():
            param.requires_grad = True

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=ff_dim,
            activation="relu",
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.output_layer = nn.Sequential(
            nn.Linear(embed_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(32, 1),
            nn.Tanh()
        )

    def forward(self, x):
        embedded_feat = self.pos2vec(x)
        embedded_feat = embedded_feat.unsqueeze(1)
        transformer_out = self.transformer_encoder(embedded_feat)  
        transformer_out = transformer_out.squeeze(1)  
        output = self.output_layer(transformer_out)

        return output
