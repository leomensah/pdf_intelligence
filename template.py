css = """
<style>
.chat-message {
    padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #4b494c;
}
.chat-message.bot {
    background-color: #748cf8;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1rem;
  color: #fff;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://pixabay.com/get/ga54d38c41faebc1e677bc8700b2d81149bca4ead49eb27f9225ace42b73a4eb61a0cfed260e0b7b9b551572da7b08c2da44a34b216c8a148255f7510df6c331dccd03013074d7830cfba5e86d3e439cc_1280.jpg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://pixabay.com/get/g7972f22975273941ef39685cc01977436358c8449eb38b606267eafb700f037ab4576e0b2e6efe9e756a35f28112d32b4a85f936e49513de681b53c9052d861320d2411ff60a35ecae2dc269164d1180_1280.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""
