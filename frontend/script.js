const backend_url = "http://127.0.0.1:5000"

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        document.getElementById('auth').style.display = 'none';
        document.getElementById('todo').style.display = 'block';
        fetchTasks();
    }
});

function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    fetch(`${backend_url}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => alert(data.message));
}

function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch(`${backend_url}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                document.getElementById('auth').style.display = 'none';
                document.getElementById('todo').style.display = 'block';
                fetchTasks();
            } else {
                alert(data.message);
            }
        });
}

function logout() {
    localStorage.removeItem('token');
    document.getElementById('auth').style.display = 'block';
    document.getElementById('todo').style.display = 'none';
}

function fetchTasks() {
    fetch(`${backend_url}/api/tasks`, {
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
        .then(response => response.json())
        .then(data => {
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';
            data.forEach(task => {
                const li = document.createElement('li');
                li.innerText = task.description;
                const deleteButton = document.createElement('button');
                deleteButton.innerText = 'Delete';
                deleteButton.onclick = () => deleteTask(task.id);
                li.appendChild(deleteButton);
                taskList.appendChild(li);
            });
        });
}

function addTask() {
    const newTask = document.getElementById('new-task').value;
    fetch(`${backend_url}/api/tasks`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify({ description: newTask })
    })
        .then(response => response.json())
        .then(() => {
            document.getElementById('new-task').value = '';
            fetchTasks();
        });
}

function deleteTask(id) {
    fetch(`${backend_url}/api/tasks/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
    })
        .then(() => fetchTasks());
}
