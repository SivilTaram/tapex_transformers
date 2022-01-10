import argparse
import torch
from transformers import ViTMAEConfig, ViTMAEFeatureExtractor, ViTMAEForPreTraining
import requests
from PIL import Image  

def rename_key(name):
    if 'patch_embed.proj' in name:
        name = name.replace('patch_embed.proj', 'embeddings.patch_embeddings.projection')
    if 'patch_embed.norm' in name:
        name = name.replace('patch_embed.norm', 'embeddings.norm')
    if 'layers' in name:
        name = 'encoder.' + name
    if 'attn.proj' in name:
        name = name.replace('attn.proj', 'attention.output.dense')
    if 'attn' in name:
        name = name.replace('attn', 'attention.self')
    if 'norm1' in name:
        name = name.replace('norm1', 'layernorm_before')
    if 'norm2' in name:
        name = name.replace('norm2', 'layernorm_after')
    if 'mlp.fc1' in name:
        name = name.replace('mlp.fc1', 'intermediate.dense')
    if 'mlp.fc2' in name:
        name = name.replace('mlp.fc2', 'output.dense')
        
    if name == 'norm.weight':
        name = 'layernorm.weight'
    if name == 'norm.bias':
        name = 'layernorm.bias'
     
    if 'head' in name:
        name = name.replace('head', 'classifier')
    else:
        name = 'vit.' + name
    
    return name

def convert_state_dict(orig_state_dict, model):    
    for key in orig_state_dict.copy().keys():
        val = orig_state_dict.pop(key)

        if 'qkv' in key:
            # TODO
            raise NotImplementedError("")
        else:
            orig_state_dict[rename_key(key)] = val
        
    return orig_state_dict

def convert_vit_mae_checkpoint(checkpoint_url, pytorch_dump_folder_path):
    config = ViTMAEConfig()
    model = ViTMAEForPreTraining(config)
    model.eval()
    
    state_dict = torch.hub.load_from_url(checkpoint_url, map_location='cpu')

    feature_extractor = ViTMAEFeatureExtractor(size = config.image_size)
    
    new_state_dict = convert_state_dict(state_dict, model)
    model.load_state_dict(new_state_dict)
    
    url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    
    image = Image.open(requests.get(url, stream=True).raw)
    feature_extractor = ViTMAEFeatureExtractor(size = config.image_size)
    inputs = feature_extractor(images=image, return_tensors="pt")
    
    print(f"Saving model to {pytorch_dump_folder_path}")
    model.save_pretrained(pytorch_dump_folder_path)
    
    print(f"Saving feature extractor to {pytorch_dump_folder_path}")
    feature_extractor.save_pretrained(pytorch_dump_folder_path)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Required parameters
    parser.add_argument(
        "--checkpoint_url",
        default="https://dl.fbaipublicfiles.com/mae/visualize/mae_visualize_vit_base.pth",
        type=str,
        help="URL of the checkpoint you'd like to convert.",
    )
    parser.add_argument(
        "--pytorch_dump_folder_path", default=None, type=str, help="Path to the output PyTorch model directory."
    )

    args = parser.parse_args()
    convert_vit_mae_checkpoint(args.checkpoint_url, args.pytorch_dump_folder_path)  