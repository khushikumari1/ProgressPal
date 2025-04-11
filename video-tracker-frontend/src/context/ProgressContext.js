// src/context/ProgressContext.js
import { createContext, useContext } from 'react';

export const ProgressContext = createContext();
export const useProgress = () => useContext(ProgressContext);
