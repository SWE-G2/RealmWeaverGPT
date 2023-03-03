var socket = io.connect("{{ url_for('socketio') }}");
socket.on('connect', function() {
    socket.emit('join', {'room': 'lobby'});
});

socket.on('message', function(data) {
    var message = data['message'];
    var chat_box = document.getElementById('chat-box');
    chat_box.innerHTML += message + '<br>';
});

function send_message() {
    var message = document.getElementById('message-box').value;
    var data = {'room': 'lobby', 'message': message};
    socket.emit('message', data);
    document.getElementById('message-box').value = '';
}
