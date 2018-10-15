from model import connect_to_db, db 
from server import app






def random_seed():    
  print('User')

    karen = User(username=‘kare’, password=’123456’, 

                  fname=‘char’, lname=‘kep’, email=‘karen@gmail.com')

    sasha = User(username=‘lensmith’, password=‘lmnop’,

                  fname=’mel’, lname=‘till’, email=‘tepp@gmail.com')

    kriss= User(username=’tek’, password=“76543”,

                  fname=‘wally’, lname=‘baker’, email=‘krisstina@gmail.com')

    tom = User(username=‘gary’, password=’98765’,

                  fname=‘cara’, lname=’walker’, email=‘sooner@gmail.com’)


    #define  ten hobbies#

def  __init__(self,name)


    hobby =  User_Hobby('foodie'),
    hobby =  User_Hobby('museums'),
    hobby =  User_Hobby('landmark'),
    hobby =  User_Hobby('dancing'),
    hobby =  User_Hobby('escape rooms'),
    hobby =  User_Hobby('wine bars'),
    hobby =  User_Hobby('dogs'),
    hobby =  User_Hobby('scenic'),
    hobby =  User_Hobby('historic'),
    hobby =  User_Hobby('kids')











    db.session.add_all([karen, sasha, kris, tom])

    db.session.commit()




    # if __name__ == '__main__':
    # connect_to_db(app)
    
    # db.create_all()