import { useEffect, useState } from 'react';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState("");
  const API_URL = "/api";

  const fetchTodos = async () => {
    const res = await fetch(`${API_URL}/items`); 
    const data = await res.json();
    setTodos(data);
  };

  useEffect(() => { fetchTodos(); }, []);

  const addTodo = async () => {
    if (!newTodo) return;
    await fetch(`${API_URL}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTodo })
    });
    setNewTodo("");
    fetchTodos();
  };

  // --- UPDATE ---
  const toggleTodo = async (id) => {
    await fetch(`${API_URL}/items/${id}`, {
      method: 'PUT'
    });
    fetchTodos();
  };

  // --- DELETE ---
  const deleteTodo = async (id) => {
    await fetch(`${API_URL}/items/${id}`, {
      method: 'DELETE'
    });
    fetchTodos();
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', maxWidth: '500px' }}>
      <h1>My DevOps Todo</h1>
      <div style={{ marginBottom: '20px' }}>
        <input 
          value={newTodo} 
          onChange={(e) => setNewTodo(e.target.value)} 
          placeholder="Что нужно сделать?" 
        />
        <button onClick={addTodo}>Добавить</button>
      </div>
      
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {todos.map(todo => (
          <li key={todo.id} style={{ marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '10px' }}>
            {/* Кнопка-галочка */}
            <input 
              type="checkbox" 
              checked={todo.completed} 
              onChange={() => toggleTodo(todo.id)} 
            />
            
            <span style={{ textDecoration: todo.completed ? 'line-through' : 'none', flexGrow: 1 }}>
              {todo.title}
            </span>

            <small style={{ color: todo.completed ? 'green' : 'orange' }}>
               {todo.completed ? "[ok]" : "[in progress]"}
            </small>

            {/* Кнопка удаления */}
            <button onClick={() => deleteTodo(todo.id)} style={{ color: 'red' }}>×</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;