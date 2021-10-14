from flask import render_template,flash,redirect,url_for,abort,request
from wtforms.validators import Email
from CleanBlog import app,db,mail,Message
from CleanBlog.forms import ContactForm, RegisterForm,LoginForm,PostForm
from CleanBlog.models import User,Post,Contact
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/")
@app.route("/home")
def index():
    sayfa=request.args.get('sayfa',1,type=int)
    posts=Post.query.order_by(Post.id.desc()).paginate(page=sayfa,per_page=3)
    sonra_url=url_for('index',sayfa=posts.next_num) if posts.has_next else None
    once_url=url_for('index',sayfa=posts.prev_num) if posts.has_prev else None
    return render_template("index.html",title='HOME',posts=posts,next_url=sonra_url,prev_url=once_url)

@app.route("/about")
def about():
    return render_template("about.html",title='ABOUT')

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        kullanici=User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(kullanici)
        db.session.commit()
        flash(f'{form.name.data} account created','success')
        return redirect(url_for('login'))

    return render_template("register.html",title='REGISTER',form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        kullanici=User.query.filter_by(email=form.email.data).first()
        if kullanici and kullanici.password==form.password.data:
            login_user(kullanici)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful','danger')
    return render_template("login.html",title='LOGIN',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/post/new",methods=["GET","POST"])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,subtitle=form.subtitle.data,post_text=form.post_text.data,user=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post is created ','success')
        return redirect(url_for('index'))
    return render_template("create_post.html",title='NEW POST',form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template("post.html",title='post.title',post=post)

@app.route("/post/<int:post_id>/edit",methods=["GET","POST"])
@login_required
def editpost(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        post.post_text=form.post_text.data
        db.session.commit()
        flash(f'Post is edited','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.subtitle.data=post.subtitle
        form.post_text.data=post.post_text
        form.submit=form.submitedit
        return render_template("create_post.html",title='EDIT POST',form=form)

@app.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def deletepost(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post is deleted','danger')
    return redirect(url_for('index'))

@app.route("/contact",methods=["GET","POST"])
def contact():
    form=ContactForm()
    if request.method=="POST":
        if form.validate_on_submit():
            contactadd=Contact(name=form.name.data, email=form.email.data, phone=form.phone.data,contact_text=form.contact_text.data)
            db.session.add(contactadd)
            db.session.commit()
            msg=Message(form.name.data,sender="CleanBlog Contact Form",recipients=["fikretba@gmail.com"])
            msg.body="""
            From: %s
            <%s>
            %s""" % (form.email.data,form.phone.data,form.contact_text.data)
            # mail.send(msg)
            flash(f'{form.name.data} opinion message has been sent','success')
            return redirect(url_for('contact'))
        else:
            flash(f'{form.name.data} opinion message has been sent','success')
    elif request.method=="GET":
        return render_template("contact.html",title='CONTACT',form=form)