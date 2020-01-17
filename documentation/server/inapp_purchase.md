# In App Purchase Pipeline

The goal of this document is to describe the basic pipeline required to implement in app purchases.

**Table of Contents**
* [Introduction](#Introduction)
* [Registering the Product](#Register)
* [Client Implementation](#Client-Implementation)
* [Server Implementation](#Server-Implementation)


# Introduction

The implementation for in app purchases differs depending on the channel used to process the transaction.
For example, the implementation for Android phones using the Google Play market is different from an iPhone.
However, the general pipeline required by all platforms will be very similar.

# Register

The first step with in-app purchases is to register the product with the payment backend.
This can be done from the developer console online.
appstoreconnect.apple.com is an example of a developer console.
Here, you add information about the item you want to offer as an in-app purchase.
This is also where you set the pricing information about the item.

# Client Implementation

Each client implementation is store independent.
Popular stores, such as the Google Play, and iOS APP Store will provide good mobile APIs to create payment dialogs.
There are Unity plugins that aid with cross-platform store implementations.
These client implementation handle the collection of payment from the user.
After a user has paid, the store backend will generate a token.
This token acts as a receipt for the transaction.
At this point, the client should send our server that token.
Once our server has completed its job, the client needs to mark the transaction as complete.

# Server Implementation

Once the client sends the receipt token to our server, we need to validate it.
We can call the issuing store's API to check the status of the receipt.
This API call can verify if the user has actually paid for an item.
Assuming the API validates the client's receipt token, we can give the purchased item to the client.
We will notify the client that the transaction was verified and completed by our server.
The server can also optionally add the receipt to a database, or Redis to keep track of completed transactions.
