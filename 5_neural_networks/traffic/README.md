# Problem Set 50: Traffic
In this project, I had to dive into the world of computer vision, utilizing the capabilities of deep learning to classify traffic signs. By employing TensorFlow and Keras, the project required preprocessing a dataset containing images of traffic signs, constructing a convolutional neural network (CNN), and training the model for accurate sign categorization. The primary objective was to gain both a solid understanding of computer vision methodologies and hands-on experience in neural network training, leading to the creation of a model capable of precisely identifying different traffic signs from images.

Two functions were left for implementation:

1. "load_data":This function is a dataset processor. It takes in a directory path, extracts and resizes images to uniform dimensions, then returns these images as arrays with their corresponding labels using OpenCV-Python module.
2. "get_model": This function defines the neural network architecture for traffic sign identification. It crafts a compiled model, where its inner structure, including layer types and quantities, filter sizes, and dropout rates, is open for customization.

Below is the implementation journey. It captures the strategies employed, challenges faced, and insights gained during the experimenation phase.

## Experimentation Process

I began my exploration with the architecture presented in the lecture. For the large dataset, this initial approach yielded a modest 5.63% accuracy. However, when I tested it with the smaller dataset, the accuracy soared to 100%, and the model ran considerably faster. Due to this stark contrast in accuracy between the two datasets, I decided to focus exclusively on optimizing the model using the larger dataset from this point onward.

The first modification I made was to lower the dropout value from 0.5 to 0.25. The accuracy remained almost the same at 5.47%. Given that lower dropout values can potentially lead to overfitting and the accuracy difference was negligible, I reverted to the original 0.5 dropout value.

Subsequently, I introduced an additional hidden layer identical to the one already implemented. However, the accuracy remained low at 5.58%. To keep the model straightforward and given the marginal difference in accuracy, I decided to stick with the original configuration of just one hidden layer.

My next step was to experiment with the approach discussed in the lecture, involving the addition of an extra convolutional and pooling layer. This change resulted in a remarkable accuracy boost to 95.90%.

Curious to understand which of the two layers, the second convolutional or the second pooling layer, was responsible for this substantial increase in accuracy, I began by removing one of the recently added layers at a time. Starting with the second pooling layer, I achieved an accuracy of 94.89%.

However, when I removed the second convolutional layer while keeping the second pooling layer, the accuracy plummeted back to 5.42%. This observation led me to conclude that the implementation of a second convolutional layer significantly contributes to the accuracy boost, whereas the second pooling layer does not. For simplicity, I decided to retain the model architecture with just a convolutional, pooling, and convolutional layer.

Next, I experimented with changing the filter size of both convolutional layers from 32 to 64, which surprisingly led to a decrease in accuracy to 89.01%. While still relatively high, this result was lower than the 95% accuracy achieved with a filter size of 32.

In further exploration, I attempted different configurations, such as 32 in the first layer and 64 in the second layer, which yielded an impressive 96.72% accuracy. Interestingly, reversing the filter sizes to 64 in the first layer and 32 in the second layer also resulted in high accuracy at 96.47%. I chose to keep the first layer with 32 and the second with 64 as it seemed more intuitive, as there is a gradual increase in complexity, although I acknowledge that the empirical rationale behind this choice is not entirely clear to me.

Further tweaks included adjusting kernel sizes in the convolutional layers, where I found that leaving them at 3x3 yielded better results compared to other sizes.

I also experimented with changing the pooling size from 2x2 to 4x4, which resulted in an accuracy of 95.28% and notably faster training.

Additionally, I added a second hidden layer with a dropout of 0.75, but this caused a drastic drop in accuracy to 5.54%. Reducing the second layer's dropout to 0.25 didn't yield significant improvements, with an accuracy of 90.00%. Hence, I removed the second hidden layer from the model.

Finally, I increased the number of neurons in the hidden layer from 128 to 256, which resulted in an accuracy of 95.69%. However, the improvement was marginal, so I decided to stick with 128 neurons.

The final model achieved a balance between speed and accuracy, making it a suitable choice for the task at hand. These experiments helped me gain insights into various factors affecting convolutional neural network performance.