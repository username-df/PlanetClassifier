import torch
from model import model, lossfn, optimizer
from torchmetrics import Accuracy
from create_dataset import train_data, test_data

accfn = Accuracy(task="multiclass", num_classes=8)

epochs = 100

for epoch in range(epochs):
    #------------- Train ----------------
    train_loss, train_acc = 0,0
    model.train()

    for X,y in train_data:
        prd = model(X)

        loss = lossfn(prd, y)
        train_loss += loss

        train_acc += accfn(y, prd.argmax(dim=1)).item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    train_loss /= len(train_data)
    train_acc /= len(train_data)

    # --------------- Test ----------------------
    test_loss, test_acc = 0, 0
    model.eval()

    with torch.inference_mode():
        testprd = model(X)

        test_loss += lossfn(testprd, y)
        test_acc += accfn(y, testprd.argmax(dim=1)).item()

        test_loss /= len(test_data)
        test_acc /= len(test_data)
    
    print(f"---------------- Epoch {epoch} ---------------------")

    print(f"Train Loss: {train_loss:.2f} | Train Accuracy: {train_acc:.2f}%\n")

    print(f"Test loss: {test_loss:.2f} | Test Accuracy: {test_acc:.2f}%\n")

    print()