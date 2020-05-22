import torch
class PhysioNet(torch.nn.Module):
    def __init_(self):
        super(PhysioNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=1, out_channels=4, kernel_size=6, padding=1)
        self.act1 = torch.nn.functional.LeakyReLU()
        self.pool1 = torch.nn.AvgPool2d(kernel_size=2, stride=2)
       
        self.conv2 = torch.nn.Conv2d(in_channels=4, out_channels=4, kernel_size=5, padding=1)
        self.act2 = torch.nn.functional.LeakyReLU()
        self.pool2 = torch.nn.AvgPool2d(kernel_size=2, stride=2)
  
        self.conv3 = torch.nn.Conv2d(in_channels=4, out_channels=10, kernel_size=4, padding=1)
        self.act3 = torch.nn.functional.LeakyReLU()        
        self.pool3 = torch.nn.AvgPool2d(kernel_size=2, stride=2)
        
        self.conv4 = torch.nn.Conv2d(in_channels=10, out_channels=10, kernel_size=4, padding=1)
        self.act4 = torch.nn.functional.LeakyReLU()
        self.pool4 = torch.nn.AvgPool2d(kernel_size=2, stride=2)

        self.conv5 = torch.nn.Conv2d(in_channels=10, out_channels=15, kernel_size=4, padding=1)
        self.act5 = torch.nn.functional.LeakyReLU()
        self.pool5 = torch.nn.AvgPool2d(kernel_size=2, stride=2)

        self.fc1 = torch.nn.Linear(15*10*10, 50)
        self.act6 = torch.nn.functional.LeakyReLU()
        self.fc2 = torch.nn.Linear(50, 20)
        self.act7 = torch.nn.functional.LeakyReLU()
        self.fc3 = torch.nn.Linear(20, 2)


        def forward(self, x):
            x = self.conv1(x)
            x = self.act1(x)    
            x = self.pool1(x)

            x = self.conv2(x)
            x = self.act2(x)
            x = self.pool2(x)

            x = self.conv3(x)
            x = self.act3(x)
            x = self.pool3(x)

            x = self.conv4(x)
            x = self.act4(x)
            x = self.pool4(x)

            x = self.conv5(x)
            x = self.act5(x)
            x = self.pool5(x)

            x = x.view(x.size(0), x.size(1)*x.size(2)*x.size(3))

            x = self.fc1(x)
            x = self.act6(x)
            x = self.fc2(x)
            x = self.act7(x)
            x = self.fc3(x)

            return x

