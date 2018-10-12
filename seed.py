from model import connect_to_db, db 
from server import app






def random_seed():    
print('User')

    karen = User(username=‘karenanderson’, password=’123456’, 

                  fname=‘char’, lname=‘kep’, email=‘forever@outlk.com')

    sasha = User(username=‘lensmith’, password=‘lmnop’,

                  fname=’mel’, lname=‘till’, email=‘tepp@gmail.com')

    kris = User(username=’tek’, password=“76543”,

                  fname=‘wally’, lname=‘baker’, email=‘mora@gmail.com')

    tom = User(username=‘gary’, password=’98765’,

                  fname=‘cara’, lname=’walker’, email=‘sooner@gmail.com’)



    db.session.add_all([karen, sasha, kris, tom])

    db.session.commit()




    # if __name__ == '__main__':
    # connect_to_db(app)
    
    # db.create_all()