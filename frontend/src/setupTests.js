import { render, screen } from '@testing-library/react';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

expect.extend(matchers);

// --- Очистка DOM после каждого теста --- 
afterEach(() => {
  cleanup();
});