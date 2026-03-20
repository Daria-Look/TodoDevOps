import { render, screen } from '@testing-library/react';
import { expect, test, vi } from 'vitest';
import App from './App';

// --- Имитация fetch, чтобы тест не ломился в реальную базу --- 
global.fetch = vi.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([{ id: 1, title: 'Mock Task', completed: false }]),
  })
);

test('Проверка: заголовок и поле ввода отображаются', async () => { render(<App />);
  
  // --- Проверка заголовка --- 
  const headerElement = screen.getByText(/My DevOps Todo/i);
  expect(headerElement).toBeInTheDocument();

  // --- Проверка наличия кнопки "Добавить" --- 
  const buttonElement = screen.getByText(/Добавить/i);
  expect(buttonElement).toBeInTheDocument();

  // --- Проверка, что имитированная задача отрисовалась --- 
  const todoItem = await screen.findByText(/Mock Task/i);
  expect(todoItem).toBeInTheDocument();
});