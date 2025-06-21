import streamlit as st

st.set_page_config(page_title="Login Page", layout="centered")

# Injecting CSS and HTML
st.markdown("""
<style>
.container {
    display: flex;
    width: 800px;
    margin: 50px auto;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 0 30px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', sans-serif;
}
.left {
    background: linear-gradient(to bottom right, #ff512f, #dd2476);
    color: white;
    flex: 1;
    padding: 50px;
    text-align: center;
}
.left h2 {
    font-size: 28px;
    margin-bottom: 10px;
}
.left p {
    font-size: 16px;
    margin-bottom: 30px;
}
.left button {
    background: transparent;
    border: 2px solid white;
    color: white;
    padding: 10px 25px;
    border-radius: 30px;
    font-size: 16px;
    cursor: pointer;
}
.right {
    background-color: white;
    flex: 1;
    padding: 50px;
    text-align: center;
}
.right h2 {
    font-size: 26px;
    margin-bottom: 20px;
    font-weight: bold;
}
.social-icons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-bottom: 20px;
}
.social-icons img {
    width: 34px;
    height: 34px;
    cursor: pointer;
    transition: transform 0.2s;
}
.social-icons img:hover {
    transform: scale(1.1);
}
.input-field {
    margin-bottom: 15px;
}
input[type=text], input[type=password] {
    width: 100%;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ddd;
    font-size: 14px;
}
.right button {
    background-color: #ff512f;
    color: white;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 30px;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
}
</style>

<div class="container">
    <div class="left">
        <h2>Welcome Back!</h2>
        <p>To keep connected with us please login<br>with your personal info.</p>
        <button onclick="alert('Login Panel!')">SIGN IN</button>
    </div>
    <div class="right">
        <h2><strong>Create Account</strong></h2>
        <div class="social-icons">
            <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn" title="LinkedIn"></a>
            <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/124/124010.png" alt="Facebook" title="Facebook"></a>
            <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/300/300221.png" alt="Google" title="Google"></a>
        </div>
        <p>or use your email for registration</p>
        <div class="input-field">
            <input type="text" placeholder="Name">
        </div>
        <div class="input-field">
            <input type="text" placeholder="Email">
        </div>
        <div class="input-field">
            <input type="password" placeholder="Password">
        </div>
        <button>SIGN UP</button>
    </div>
</div>
""", unsafe_allow_html=True)
