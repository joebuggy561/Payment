from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
from decimal import Decimal



@login_required
def search_user_by_account_number(request):
    # account = Account.objects.filter(account_status="active")
    account = Account.objects.all()
    query = request.POST.get("account_number")
    print(query)
    if query:
        account = account.filter(
        Q(account_number=query)|
        Q(account_id=query)
        ).distinct()
    context = {
        "account":account,
        "query":query,
    }
    return render(request, "transfer/search-user-by-account-number.html", context)


def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "Account does not exist")
        return redirect("core:search-account")
    context = {
        "account":account,
    }
    return render(request, "transfer/amount_transfer.html", context)



def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    reciever = account.user


    sender_account = request.user.account
    reciever_account = account


    if request.method=="POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.account_balance > Decimal(amount):
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                reciever = reciever,
                sender = sender,
                reciever_account = reciever_account,
                sender_account = sender_account,
                status = "processing",
                transaction_type = "transfer",
            )

            new_transaction.save()

        #get the id of the transaction that was created now

            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
    
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("core:amount-transfer", account.account_number)
        
    else:
        messages.warning(request, "Error Occured, Try again later.")
        return redirect("account:account")
    

def TransferConfirmation(request, account_number, transaction_id):

    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist")
        return redirect ("account:account")


    context = {
        "account":account,
        "transaction": transaction,
    }

    return render(request, "transfer/transfer_confirmation.html", context)
    



def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user 
    reciever = account.user

    sender_account = request.user.account 
    reciever_account = account

    completed = False

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print (pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            #remove the amount I am sending from my account balance
            sender_account.account_balance -= transaction.amount
            sender.save()

            #Add the amount that was removed from the person I am sending the money too
            account.account_balance += transaction.amount
            account.save()

            messages.success(request, "Transfer Sucessful!")
            return redirect("core:transfer-completed",  account.account_number, transaction.transaction_id)

        else:
            messages.warning(request, "Incorrect Pin")
            return redirect("core:transfer-confirmation", account.account_number, transaction.transaction_id) ##try and limit number of times of pin entry
    
    else:
        messages.warning(request, "An error occured, try again later")
        return redirect("account:account")






def TransferCompleted(request, account_number, transaction_id):

    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist")
        return redirect ("account:account")


    context = {
        "account":account,
        "transaction": transaction,
    }

    return render(request, "transfer/transfer_completed.html", context)





    

 

