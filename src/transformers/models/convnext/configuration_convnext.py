# coding=utf-8
# Copyright 2022 Facebook AI and The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" ConvNeXT model configuration"""

from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

CONVNEXT_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "facebook/convnext-tiny-224": "https://huggingface.co/facebook/convnext-tiny-224/resolve/main/config.json",
    # See all ConvNeXT models at https://huggingface.co/models?filter=convnext
}


class ConvNextConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a [`~ConvNextModel`]. It is used to instantiate an
    ConvNeXT model according to the specified arguments, defining the model architecture. Instantiating a configuration
    with the defaults will yield a similar configuration to that of the ConvNeXT
    [facebook/convnext-tiny-224](https://huggingface.co/facebook/convnext-tiny-224) architecture.

    Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
    documentation from [`PretrainedConfig`] for more information.

    Args:
        num_channels (`int`, *optional*, defaults to `3`):
            The number of input channels.
        num_stages (`int`, optional, defaults to 4):
            The number of stages in the model.
        dims (`List[int]`, *optional*, defaults to [96, 192, 384, 768]):
            Dimensionality of each stage.
        depths (`List[int]`, *optional*, defaults to [3, 3, 9, 3]):
            Depth (number of blocks) for each stage.
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        layer_norm_eps (`float`, *optional*, defaults to 1e-12):
            The epsilon used by the layer normalization layers.
        layer_scale_init_value (`float`, *optional*, defaults to 1e-6):
            The initial value for the layer scale.
        drop_path_rate (`float`, *optional*, defaults to 0.0):
            The drop rate for stochastic depth.

    Example:
    ```python
    >>> from transformers import ConvNextModel, ConvNextConfig

    >>> # Initializing a ConvNext convnext-tiny-224 style configuration
    >>> configuration = ConvNextConfig()
    >>> # Initializing a model from the convnext-tiny-224 style configuration
    >>> model = ConvNextModel(configuration)
    >>> # Accessing the model configuration
    >>> configuration = model.config
    ```"""
    model_type = "convnext"

    def __init__(
        self,
        num_channels=3,
        num_stages=4,
        dims=[96, 192, 384, 768],
        depths=[3, 3, 9, 3],
        initializer_range=0.02,
        layer_norm_eps=1e-12,
        is_encoder_decoder=False,
        layer_scale_init_value=1e-6,
        drop_path_rate=0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.num_channels = num_channels
        self.num_stages = num_stages
        self.dims = dims
        self.depths = depths
        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps
        self.layer_scale_init_value = layer_scale_init_value
        self.drop_path_rate = drop_path_rate