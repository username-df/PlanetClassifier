import torch
from convModel import model, lossfn, optimizer
from create_dataset import train_data, val_data, test_data
import matplotlib.pyplot as plt

accfn = lambda y, prd: ((y == prd.argmax(dim=1)).sum()) / len(prd)

epochs = 15

def loss_curves(epochs, train, test):
    xs = range(1, epochs+1)
    plt.plot(xs, train, 'b-', label="Train Loss")
    plt.plot(xs, test, 'b--', label="Test Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

train_hst, val_hst = [], []

for epoch in range(epochs):
    #------------- Train ----------------
    train_loss, train_acc = 0, 0
    
    for X,y in train_data:
        model.train()

        trainprd = model(X)

        loss = lossfn(trainprd, y)

        train_loss += loss
        train_acc += accfn(y, trainprd).item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    train_loss /= len(train_data)
    train_acc /= len(train_data)

    # --------------- Validation ----------------------
    val_loss, val_acc = 0, 0
    model.eval()

    with torch.inference_mode():
        for X,y in val_data:
            valprd = model(X)

            val_loss += lossfn(valprd, y)
            val_acc += accfn(y, valprd).item()

        val_loss /= len(test_data)
        val_acc /= len(test_data)

    model.save(file_name=f"saved{epoch}.pth")

    train_hst.append(train_loss.item())
    val_hst.append(val_loss.item())

    print(f"---------------- Epoch {epoch} ---------------------")

    print(f"Train Loss: {train_loss:.2f} | Train Accuracy: {train_acc*100:.2f}%\n")

    print(f"Validation loss: {val_loss:.2f} | Validation Accuracy: {val_acc*100:.2f}%\n")

    print()


loss_curves(epochs, train_hst, val_hst)

# --------------- Test ----------------------
test_loss, test_acc = 0, 0
model.eval()

with torch.inference_mode():
    for X,y in test_data:
        testprd = model(X)

        test_loss += lossfn(testprd, y)
        test_acc += accfn(y, testprd).item()

    test_loss /= len(test_data)
    test_acc /= len(test_data)

print(f"---------------- Testing ---------------------")
print(f"Test loss: {test_loss:.2f} | Test Accuracy: {test_acc*100:.2f}%\n")