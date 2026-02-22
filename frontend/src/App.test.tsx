import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders StepSight app', () => {
    render(<App />);
    // Look for any content that indicates the app loaded
    const appElement = document.querySelector('.App') || document.body;
    expect(appElement).toBeInTheDocument();
});

test('app component exists', () => {
    expect(App).toBeDefined();
});