import json
import pdb


def products_to_dict(product_list):
    inventory = {}
    for product in product_list:
        inventory[product['productId']] = product

    return inventory


def process_orders(orders, inventory):
    # Check that an order can be fulfilled completetly before fulfilling any
    # individual items and adjust stock levels
    unfulfillable = []
    for order in orders:
        print(order['orderId'])
        can_fulfill = True
        id = None
        quantity = None
        for item in order['items']:
            on_hand  = inventory[item['productId']]['quantityOnHand']
            id = item['productId']
            quantity = item['quantity']
            print(f'\t{id} x {quantity} - on hand: {on_hand}')

            if item['quantity'] > on_hand:
                can_fulfill = False

        print(f'can fulfull: {can_fulfill}')

        # adjust the stock levels, create a list of unfulfillable IDs
        if can_fulfill:
            for item in order['items']:
                id = item['productId']
                quantity = item['quantity']
                on_hand  = inventory[id]['quantityOnHand']
                inventory[id]['quantityOnHand'] = on_hand - quantity
        else:
            order['status'] = 'Unfulfillable'
            unfulfillable.append(order['orderId'])

    return unfulfillable


def reorder(inventory):
    # order low stock
    products_order_pending = []
    for product in inventory.values():
        try:
            on_hand = product['quantityOnHand']
            threshold = product['reorderThreshold']
            if on_hand < threshold:
                # need to also check that there's not a pending purchase order
                id = product['productId']
                quantity = product['reorderAmount']
                print(f'Reorder item {id} x {quantity}')
                products_order_pending.append(id)
        except KeyError:
            print(f'Error re-ordering item')
            print(product)
    return products_order_pending


#  Main process
data_file = open('data.json')
data = json.load(data_file)

inventory = products_to_dict(data['products'])
orders = data['orders']
unfulfillable = process_orders(orders, inventory)

print('\nUnfillable orders:')
for order in unfulfillable:
    print(f'\t{order}')

reorder(inventory)
