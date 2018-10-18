from model import connect_to_db, db, User, Hobby, User_Hobby


def seed():

    db.create_all()

    User.query.delete()
    Hobby.query.delete()
    User_Hobby.query.delete()

    karen = User(username='kare', password='12345600', fname='char',
                 lname='kep', email='karen@gmail.com')

    sasha = User(username='lensmith', password='lmnop000',
                 fname='mel', lname='till', email='tepp@gmail.com')

    kris = User(username='tek', password='7654300', fname='wally',
                lname='baker', email='krisstina@gmail.com')

    tom = User(username='gary', password='98765000', fname='cara',
               lname='walker', email='sooner@gmail.com')

    hobby1 = Hobby(name='foodie')
    hobby2 = Hobby(name='museums')
    hobby3 = Hobby(name='landmark')
    hobby4 = Hobby(name='dancing')
    hobby5 = Hobby(name='escape rooms')
    hobby6 = Hobby(name='wine bars')
    hobby7 = Hobby(name='dogs')
    hobby8 = Hobby(name='scenic')
    hobby9 = Hobby(name='historic')
    hobby10 = Hobby(name='kids')
    hobby11 = Hobby(name='shopping')

    db.session.add_all([karen, sasha, kris, tom,
                        hobby1, hobby2, hobby3, hobby4, hobby5,
                        hobby6, hobby7, hobby8, hobby9, hobby10, hobby11 ])

    db.session.commit()

    karen.hobbies.extend([hobby3, hobby6, hobby9])
    tom.hobbies.extend([hobby8, hobby5])
    kris.hobbies.extend([hobby1, hobby7])
    sasha.hobbies.extend([hobby4, hobby7, hobby5])

    db.session.commit()


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    seed()
