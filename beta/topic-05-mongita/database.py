from mongita import MongitaClientDisk
from bson.objectid import ObjectId
client = MongitaClientDisk()

db = client.shopping_list_db

def setup_database():
    db.drop_collection(db.item_collection)
    item_collection = db.item_collection

    for description in ['apples', 'broccoli', 'pizza', 'tangerines', 'potatoes']:
        item_collection.insert_one({"description":description})

def get_items(id=None):
    item_collection = db.item_collection
    if id == None:
        items = list(item_collection.find({}))
        for item in items:
            item['id'] = str(item['_id'])
    else:
        try:
            id = ObjectId(id)
            items = list(item_collection.find({"_id":id}))
            #items['id'] = str(items['_id'])
            # items = [
            #     { 
            #         "id" : item.id,
            #         "description" : item.description
            #     }
            #     for item in items
            # ]
            for item in items:
                item['id'] = str(item['_id'])

        except Exception as e:
            print(e)
    return items


def add_item(description):
    item_collection = db.item_collection
    #item = Item(description=description)
    item_collection.insert_one({"description":description})

def delete_item(id):
    item_collection = db.item_collection
    #item = Item.select().where(Item.id == id).get()
    
    id = ObjectId(id)
    item_collection.delete_one({"_id":id})

   
def update_item(id, description):
    # item = Item.select().where(Item.id == id).get()
    # item.description = description
    # item.save()
    #Item.update({Item.description: description}).where(Item.id == id).execute()
    id = ObjectId(id)
    item_collection = db.item_collection
    item_collection.update_one({'_id':id},{'$set':{'description':description}})

def test_setup_database():
    print("testing setup_database()")
    setup_database()
    items = get_items()
    assert len(items) == 5
    descriptions = [item['description'] for item in items]
    for description in ['apples', 'broccoli', 'pizza', 'tangerines', 'potatoes']:
        assert description in descriptions

def test_get_items():
    print("testing get_items()")
    setup_database()
    items = get_items()
    assert type(items) is list
    assert len(items) > 0
    for item in items:
        assert '_id' in item
        # assert type(item['id']) is int
        assert 'description' in item
        assert type(item['description']) is str
#     example_id = items[0]['id']
#     example_description = items[0]['description']
#     items = get_items(example_id)
#     assert len(items) == 1
#     assert example_id == items[0]['id']
#     assert example_description == items[0]['description']

def test_add_item():
    print("testing add_item()")
    setup_database()
    items = get_items()
    original_length = len(items)
    add_item("licorice")
    items = get_items()
    assert len(items) == original_length + 1
    descriptions = [item['description'] for item in items]
    assert "licorice" in descriptions

def test_delete_item():
    print("testing delete_item()")
    setup_database()
    items = get_items()
    original_length = len(items)
    deleted_description = items[1]['description']
    deleted_id = items[1]['_id']

    delete_item(delete_item)
    items = get_items()
    assert len(items) == original_length - 1 
    for item in items:
        assert item['id'] != deleted_id
        assert item['description'] != deleted_description

def test_update_item():
    print("testing update_item()")
    setup_database()
    items = get_items()
    original_description = items[1]['description']
    original_id = items[1]['_id']
    update_item(original_id,"new-description")
    items = get_items()
    found = False
    for item in items:
        if item['_id'] == original_id:
            assert item['description'] == "new-description"
            found = True
    assert found

if __name__ == "__main__":
    test_setup_database()
    test_get_items()
    test_add_item()
    test_delete_item()
    test_update_item()
    print("done.")
