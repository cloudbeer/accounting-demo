import axios from 'axios';
import type { Transaction, TransactionCreate } from '../types';

const api = axios.create({
    baseURL: 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const createTransaction = async (data: TransactionCreate) => {
    const response = await api.post('/transactions/', data);
    return response.data;
};

export const createTransactionFromText = async (text: string) => {
    const response = await api.post('/transactions/natural', { text });
    return response.data;
};

export const getTransactions = async () => {
    const response = await api.get('/transactions/');
    return response.data;
};

export const getStatistics = async (days: number = 30) => {
    const response = await api.get(`/statistics/?days=${days}`);
    return response.data;
};

export const deleteTransaction = async (id: number) => {
    const response = await api.delete(`/transactions/${id}`);
    return response.data;
};