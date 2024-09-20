# Malaria Cell Classification:
The dataset I'll be training on was compiled by the NIH, it was derived from nine studies examining 714 patients. These studies assembled 27,558 images of cells that were either healthy or infected with malaria. The images used for training were created through capturing images through an eyepiece of a microscope and then processing them through a series of [neural networks](https://ieeexplore.ieee.org/document/9244549). A few cells can be seen here:

<div align="center">
  <img src="images/cells.png" alt="cell image" width="500"> 
</div>


I set out to train a network that examines the processed cells to determine whether or not they are infected with malaria. To begin, I examined the proportions of the cells present, and the proportions were exactly equal:

| Class    |Image Count|Proportion|
|----------|----------|----------|
| Infected | 13779    | 0.50     |
|Uninfected| 13779    |0.50      |

# Experiment 0: 
My first model had resnet34 architecture adjusted to compensate for just 2 classes. Additionally, the model came with pretrained weights, with the weight set orignating from ImageNet-1K. The training was remarkably fast with the accuracy improving to around 97% after just two epochs. However, I had my training set to 5 epochs and subsequent epochs led to possible overfitting, with training accuracy higher than my testing accuracy, and my training loss lower than testing loss.
### Accuracy Plot:
<div align="center">
  <img src="models/experiment0/accuracy_plot.png" alt="accuracy plot">
</div>

### Loss Plot:
<div align="center">
  <img src="models/experiment0/loss_plot.png" alt="accuracy plot">
</div>

### Future Directions:
* I noticed that the network trained quickly, in fact after 2 epochs the training accuracies and losses diverged. To compensate for this, I'll either reduce the model complexity of my current architecure and maintain the current epoch count or decrease epochs and maintain the current model complexity.

# Experiment 1: 
The first model displayed fast training and quick diveregence. So for this experiment I decided to decrease epoch count while maintaining the current model complexity. This model showed impressive metrics, however, I think the metrics I'm using to evaluate my model could be expanded upon.

### Accuracy Plot:
<div align="center">
  <img src="models/experiment1/accuracy_plot.png" alt="accuracy plot">
</div>

### Loss Plot:
<div align="center">
  <img src="models/experiment1/loss_plot.png" alt="accuracy plot">
</div>

### Future Directions:
1) I want to explore other metrics. While loss and accuracy good measures to have in an arsenal of other measures, it shouldn't be the only measures used. I want to include confusion matrices, recall, precision, and specificity. I plan on adding these measures in future experiments. Additionally, If I'm looking to deploy these models, I want to have greater certainty and that can only be obtained through a more nuanced and in-depth evaluation phase.
2) Due to the rapid divergence, I may want to reduce the complexity of my CNN to resnet18 and increase the epochs of which it's trained on. This may help for better generalization to novel image sets.

# Experiment 2:
I switched to higher epochs and lowered the complexity of the network as highlighted in the future directions of the previous experiment. Additionally, I added more measures to examine the different facets of the model's prediction capacities. The model trained well, reaching around 96% for accuracy, recall, precision, and speceficity. Additionally, the confusion matrix highlighted that while there is some error, the model is able to differentiate between positive cases and negative cases effectively. 

### Model Metrics:
<div align="center">
  <img src="models/experiment2/metrics_comparison.png" alt="accuracy plot">
</div>

### Future directions:
* Now that I have access to more diagnostic criteria, I want to begin to tune the model accordingly. In this circumstance, false negatives have a much more drastic outcomes, an undiagnosed patient would miss vital treatments and contribute to the propogation of disease. With this in mind, I want to incur data manipulations prior to the training phase that bias the model in a direction that minimizes false negatives. While this will increase the likelihood of false positives, a false positive would have less dire consequences.