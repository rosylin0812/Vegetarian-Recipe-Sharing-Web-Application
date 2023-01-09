from flask import Blueprint, render_template, request, redirect, abort
from veggyblog.models import Post, PostSaved, User, follows
from flask_login import current_user, login_required
from veggyblog import db
from veggyblog.users.forms import EmptyForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home", methods = ["GET", "POST"])
def home():
    page = request.args.get('page', 1, type=int)
    if request.method == "POST":
                
        input = request.form['search']
        search = "%{}%".format(input)
        
        posts = Post.query.filter(Post.title.like(search) | Post.content.like(search)).\
            order_by(Post.date_posted.desc()).paginate(page = page, per_page = 10)
                
        return render_template('home.html', posts = posts, legend= 'search')
    
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page = 10)
        return render_template('home.html', posts = posts)

#######################    follow     ##########################
@main.route("/follows/<int:user_id>", methods = ["GET", "POST"])
@login_required
def following_users(user_id):
    page = request.args.get('page', 1, type=int)
    users = User.query.filter(User.follows.any(User.id == current_user.id))\
        .paginate(page = page, per_page = 10)
    
    return render_template('following_users.html', users = users)

@main.route('/follow/<int:user_id>', methods= ["GET", "POST"])
@login_required
def follow(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if not user:
        return ('user does not exits')
    else:
        current_user.follow(user)
        db.session.commit()
        return redirect(request.referrer)
    
@main.route('/unfollow/<int:user_id>', methods= ["GET", "POST"])
@login_required
def unfollow(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    if not user:
        return ('user does not exits')
    else:
        current_user.unfollow(user)
        db.session.commit()
    
        return redirect(request.referrer)



########################    save     ##########################
@main.route("/saved/<int:user_id>", methods = ["GET", "POST"])
@login_required
def saved(user_id):
    page = request.args.get('page', 1, type=int)
    #user = User.query.filter_by( id = current_user.id)
    posts = Post.query.join(PostSaved, Post.id==PostSaved.post_id)\
            .filter(PostSaved.user_id == current_user.id).paginate(page = page, per_page = 10)
    
    return render_template('saved_posts.html', posts = posts)

@main.route('/save/<int:post_id>', methods= ["GET", "POST"])
@login_required
def save(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if not post:
        return ('post does not exits')
    else:
        current_user.save_post(post)
        db.session.commit()
        return redirect(request.referrer)
    
@main.route('/unsave/<int:post_id>', methods= ["GET", "POST"])
@login_required
def unsave(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if not post:
        return ('post does not exits')
    else:
        current_user.unsave_post(post)
        db.session.commit()
    
        return redirect(request.referrer)




@main.route("/about-us-veggy/")
def about():
    return render_template('footer/about.html', title="About")

@main.route("/terms")
def terms():
    return render_template('footer/terms.html')

@main.route("/privacy-policy")
def privacy():
    return render_template('footer/privacy-policy.html')