import re
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Pegamos acá el log exacto que obtuviste de Colab
    log_data = """
    1/75 2.02G 1.816 5.474 1.779 0 640: 100% 43/43 3.4it/s 12.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 1.4it/s 2.1s all 83 28 0.00133 0.972 0.284 0.0843 
    2/75 2.09G 1.57 3.778 1.56 1 640: 100% 43/43 5.1it/s 8.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.674 0.392 0.365 0.2 
    3/75 2.1G 1.561 3.127 1.498 0 640: 100% 43/43 4.6it/s 9.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.839 0.55 0.532 0.274 
    4/75 2.1G 1.62 2.579 1.579 1 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.8it/s 0.8s all 83 28 0.665 0.644 0.552 0.334 
    5/75 2.1G 1.481 2.284 1.413 2 640: 100% 43/43 5.3it/s 8.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.6it/s 1.2s all 83 28 0.74 0.533 0.498 0.265 
    6/75 2.1G 1.469 1.881 1.431 1 640: 100% 43/43 5.0it/s 8.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.775 0.528 0.534 0.319 
    7/75 2.1G 1.459 1.68 1.469 1 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.0it/s 0.6s all 83 28 0.949 0.48 0.566 0.289 
    8/75 2.1G 1.481 1.606 1.423 2 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.878 0.522 0.524 0.322 
    9/75 2.1G 1.431 1.473 1.419 2 640: 100% 43/43 5.3it/s 8.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.7it/s 1.1s all 83 28 0.803 0.544 0.536 0.327 
    10/75 2.1G 1.448 1.475 1.405 1 640: 100% 43/43 5.1it/s 8.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.7it/s 0.8s all 83 28 0.989 0.544 0.594 0.355 
    11/75 2.1G 1.465 1.379 1.481 2 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.0it/s 0.7s all 83 28 0.958 0.528 0.576 0.349 
    12/75 2.1G 1.306 1.305 1.314 0 640: 100% 43/43 4.4it/s 9.8s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.6it/s 0.7s all 83 28 0.477 0.571 0.597 0.417 
    13/75 2.1G 1.352 1.193 1.376 1 640: 100% 43/43 5.1it/s 8.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.6it/s 1.1s all 83 28 0.866 0.593 0.603 0.405 
    14/75 2.1G 1.341 1.11 1.379 1 640: 100% 43/43 5.4it/s 7.9s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.1it/s 0.6s all 83 28 0.944 0.548 0.589 0.42 
    15/75 2.1G 1.305 1.058 1.333 0 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.9it/s 0.8s all 83 28 0.526 0.572 0.594 0.416 
    16/75 2.1G 1.303 1.078 1.339 1 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.8it/s 0.6s all 83 28 0.658 0.595 0.597 0.378 
    17/75 2.1G 1.351 1.023 1.36 0 640: 100% 43/43 5.2it/s 8.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.9it/s 1.0s all 83 28 0.631 0.569 0.592 0.342 
    18/75 2.1G 1.299 1.037 1.335 2 640: 100% 43/43 5.4it/s 8.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.974 0.577 0.6 0.398 
    19/75 2.1G 1.202 1.008 1.254 0 640: 100% 43/43 4.6it/s 9.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.8it/s 0.6s all 83 28 0.95 0.544 0.59 0.392 
    20/75 2.1G 1.268 0.9883 1.323 2 640: 100% 43/43 4.5it/s 9.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.986 0.578 0.599 0.402 
    21/75 2.1G 1.267 0.9931 1.315 2 640: 100% 43/43 5.2it/s 8.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.0it/s 1.0s all 83 28 0.974 0.555 0.598 0.354 
    22/75 2.1G 1.252 0.948 1.304 1 640: 100% 43/43 4.9it/s 8.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.1it/s 0.7s all 83 28 0.554 0.585 0.592 0.4 
    23/75 2.1G 1.158 0.951 1.232 0 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.1it/s 0.7s all 83 28 0.968 0.557 0.597 0.417 
    24/75 2.1G 1.158 0.9001 1.206 0 640: 100% 43/43 4.4it/s 9.8s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.0it/s 0.8s all 83 28 0.974 0.569 0.784 0.52 
    25/75 2.1G 1.134 0.843 1.229 0 640: 100% 43/43 5.1it/s 8.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.9it/s 1.0s all 83 28 0.917 0.578 0.602 0.399 
    26/75 2.1G 1.174 0.8867 1.246 0 640: 100% 43/43 5.3it/s 8.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.3it/s 0.7s all 83 28 0.942 0.578 0.606 0.409 
    27/75 2.1G 1.146 0.8034 1.204 0 640: 100% 43/43 4.7it/s 9.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.996 0.56 0.675 0.445 
    28/75 2.1G 1.12 0.8208 1.207 0 640: 100% 43/43 4.3it/s 10.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.3it/s 0.7s all 83 28 0.95 0.568 0.608 0.39 
    29/75 2.1G 1.102 0.7922 1.196 0 640: 100% 43/43 5.4it/s 8.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.2it/s 0.9s all 83 28 0.961 0.578 0.618 0.437 
    30/75 2.1G 1.142 0.8473 1.228 1 640: 100% 43/43 4.9it/s 8.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.963 0.544 0.609 0.411 
    31/75 2.1G 1.153 0.8382 1.251 1 640: 100% 43/43 4.4it/s 9.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.2it/s 0.6s all 83 28 0.987 0.593 0.627 0.402 
    32/75 2.1G 1.136 0.8405 1.23 2 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.971 0.599 0.634 0.417 
    33/75 2.1G 1.053 0.7434 1.156 0 640: 100% 43/43 5.5it/s 7.9s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.9it/s 1.0s all 83 28 0.989 0.6 0.648 0.468 
    34/75 2.1G 1.091 0.7559 1.215 1 640: 100% 43/43 4.8it/s 9.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.3it/s 0.6s all 83 28 0.947 0.571 0.62 0.443 
    35/75 2.1G 1.089 0.7599 1.207 0 640: 100% 43/43 4.5it/s 9.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.4it/s 0.7s all 83 28 0.966 0.578 0.613 0.433 
    36/75 2.1G 1.092 0.7437 1.225 1 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.981 0.556 0.611 0.418 
    37/75 2.1G 0.9823 0.7142 1.129 0 640: 100% 43/43 5.4it/s 8.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.4it/s 0.9s all 83 28 0.977 0.572 0.627 0.415 
    38/75 2.1G 1.08 0.7552 1.231 1 640: 100% 43/43 4.8it/s 8.9s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.1it/s 0.7s all 83 28 0.971 0.578 0.638 0.442 
    39/75 2.1G 1.042 0.7416 1.165 0 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.959 0.6 0.652 0.435 
    40/75 2.1G 0.9673 0.7588 1.142 1 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.992 0.572 0.612 0.428 
    41/75 2.1G 1.036 0.7897 1.197 0 640: 100% 43/43 5.6it/s 7.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.8it/s 0.8s all 83 28 0.934 0.6 0.639 0.405 
    42/75 2.1G 1.056 0.7669 1.192 2 640: 100% 43/43 4.3it/s 10.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.4it/s 0.6s all 83 28 0.985 0.585 0.607 0.429 
    43/75 2.1G 1.037 0.7341 1.179 2 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.945 0.563 0.635 0.425 
    44/75 2.1G 0.9925 0.6586 1.143 1 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.2it/s 0.9s all 83 28 0.97 0.577 0.63 0.442 
    45/75 2.1G 1.024 0.6888 1.172 1 640: 100% 43/43 5.2it/s 8.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.4it/s 0.7s all 83 28 0.938 0.622 0.661 0.461 
    46/75 2.1G 0.9217 0.631 1.109 1 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.958 0.556 0.623 0.432 
    47/75 2.1G 0.9966 0.6741 1.16 0 640: 100% 43/43 4.3it/s 10.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.0it/s 0.7s all 83 28 0.965 0.578 0.664 0.455 
    48/75 2.1G 0.9446 0.6049 1.118 0 640: 100% 43/43 4.4it/s 9.8s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.975 0.576 0.718 0.496 
    49/75 2.1G 0.9452 0.644 1.114 0 640: 100% 43/43 5.0it/s 8.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.1it/s 1.0s all 83 28 0.938 0.578 0.614 0.413 
    50/75 2.1G 0.928 0.6197 1.121 1 640: 100% 43/43 4.8it/s 9.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.6it/s 0.7s all 83 28 0.958 0.578 0.611 0.435 
    51/75 2.1G 0.8928 0.5912 1.076 0 640: 100% 43/43 4.5it/s 9.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.937 0.576 0.641 0.445 
    52/75 2.1G 0.9335 0.5882 1.109 1 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.969 0.573 0.616 0.433 
    53/75 2.1G 0.9037 0.5916 1.089 0 640: 100% 43/43 5.0it/s 8.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.9it/s 1.0s all 83 28 0.962 0.574 0.606 0.443 
    54/75 2.1G 0.8827 0.6013 1.064 0 640: 100% 43/43 5.1it/s 8.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.8it/s 0.6s all 83 28 0.932 0.578 0.658 0.452 
    55/75 2.1G 0.8959 0.6365 1.084 1 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.5it/s 0.7s all 83 28 0.933 0.599 0.643 0.452 
    56/75 2.1G 0.8305 0.5536 1.079 2 640: 100% 43/43 4.4it/s 9.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.2it/s 0.6s all 83 28 0.966 0.575 0.669 0.461 
    57/75 2.1G 0.8631 0.5818 1.08 1 640: 100% 43/43 5.2it/s 8.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.6it/s 1.1s all 83 28 0.966 0.578 0.595 0.419 
    58/75 2.1G 0.8525 0.5578 1.067 0 640: 100% 43/43 4.9it/s 8.7s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.968 0.578 0.641 0.453 
    59/75 2.1G 0.8496 0.6455 1.069 0 640: 100% 43/43 4.6it/s 9.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.4it/s 0.7s all 83 28 0.96 0.578 0.671 0.487 
    60/75 2.1G 0.8658 0.5381 1.083 2 640: 100% 43/43 4.5it/s 9.5s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.972 0.599 0.619 0.425 
    61/75 2.1G 0.856 0.5291 1.085 2 640: 100% 43/43 5.3it/s 8.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.0it/s 0.8s all 83 28 0.97 0.596 0.627 0.445 
    62/75 2.1G 0.887 0.5589 1.096 2 640: 100% 43/43 4.8it/s 9.0s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.6it/s 0.5s all 83 28 0.595 0.708 0.68 0.489 
    63/75 2.1G 0.846 0.5654 1.062 0 640: 100% 43/43 4.5it/s 9.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.3it/s 0.7s all 83 28 0.965 0.578 0.686 0.499 
    64/75 2.1G 0.8243 0.5264 1.066 2 640: 100% 43/43 4.7it/s 9.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.0it/s 1.0s all 83 28 0.604 0.933 0.697 0.483 
    65/75 2.1G 0.8227 0.4992 1.071 1 640: 100% 43/43 5.3it/s 8.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.3it/s 0.7s all 83 28 0.581 0.911 0.706 0.515 
    66/75 2.1G 0.841 0.584 1.045 0 640: 100% 43/43 4.0it/s 10.9s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.676 0.923 0.755 0.549 
    67/75 2.1G 0.7876 0.4977 1.022 0 640: 100% 43/43 4.6it/s 9.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.8it/s 0.6s all 83 28 0.602 0.823 0.755 0.56 
    68/75 2.1G 0.7501 0.4623 0.9861 0 640: 100% 43/43 4.9it/s 8.8s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 3.9it/s 0.8s all 83 28 0.973 0.573 0.741 0.533 
    69/75 2.1G 0.7814 0.4698 1.018 1 640: 100% 43/43 5.6it/s 7.6s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.7it/s 0.6s all 83 28 0.963 0.578 0.92 0.716 
    70/75 2.1G 0.7182 0.4432 0.9763 0 640: 100% 43/43 4.7it/s 9.1s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.2it/s 0.7s all 83 28 0.859 0.594 0.917 0.679 
    71/75 2.1G 0.7009 0.484 0.9633 0 640: 100% 43/43 4.7it/s 9.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 5.2it/s 0.6s all 83 28 0.843 0.578 0.914 0.679 
    72/75 2.1G 0.7165 0.4365 0.9645 0 640: 100% 43/43 5.3it/s 8.2s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 2.7it/s 1.1s all 83 28 0.865 0.578 0.925 0.685 
    73/75 2.1G 0.6973 0.4368 0.96 0 640: 100% 43/43 5.1it/s 8.4s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.9it/s 0.6s all 83 28 0.742 0.911 0.919 0.694 
    74/75 2.1G 0.695 0.4525 0.9702 0 640: 100% 43/43 4.6it/s 9.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.1it/s 0.7s all 83 28 0.862 0.911 0.922 0.705 
    75/75 2.1G 0.6932 0.4304 0.9433 0 640: 100% 43/43 4.6it/s 9.3s Class Images Instances Box(P R mAP50 mAP50-95): 100% 3/3 4.6it/s 0.6s all 83 28 0.966 0.578 0.938 0.709
    """

    epochs = []
    map50_vals = []

    # Extraer época y mAP50 con expresiones regulares
    for line in log_data.split('\n'):
        # Buscar la línea que dice "1/75 ... all 83 28 ..."
        match = re.search(r'(\d+)/75.*?all\s+\d+\s+\d+\s+[\d\.]+\s+[\d\.]+\s+([\d\.]+)', line)
        if match:
            epoch = int(match.group(1))
            map50 = float(match.group(2)) * 100  # Multiplicamos por 100 para porcentaje
            epochs.append(epoch)
            map50_vals.append(map50)

    # Configurar estilo
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Dibujar la línea
    plt.plot(epochs, map50_vals, color='#009CA6', linewidth=3, marker='o', markersize=4, label="Precisión mAP50")
    
    # Marcar el punto final (92%)
    plt.scatter(epochs[-1], map50_vals[-1], color='#CC0000', s=100, zorder=5)
    plt.annotate(f'Resultado Final:\n{map50_vals[-1]:.1f}%', 
                 xy=(epochs[-1], map50_vals[-1]), 
                 xytext=(epochs[-1] - 15, map50_vals[-1] - 10),
                 arrowprops=dict(facecolor='#333', shrink=0.05, width=1.5, headwidth=6),
                 fontsize=12, fontweight='bold', color='#333',
                 bbox=dict(boxstyle="round,pad=0.4", fc="#FFF", ec="#009CA6", lw=2))

    # Estética del gráfico
    plt.title('Curva de Aprendizaje de IA (75 Iteraciones)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Época (Iteración de Entrenamiento)', fontsize=12)
    plt.ylabel('Precisión (mAP50 %)', fontsize=12)
    plt.ylim(0, 100)
    plt.xlim(1, 75)
    
    # Rellenar bajo la curva sutilmente
    plt.fill_between(epochs, map50_vals, alpha=0.1, color='#009CA6')
    
    sns.despine()
    plt.tight_layout()
    
    # Guardar
    output = 'curva_aprendizaje.png'
    plt.savefig(output, dpi=300)
    print(f"✅ Gráfico generado con éxito: {output}")

if __name__ == '__main__':
    main()

