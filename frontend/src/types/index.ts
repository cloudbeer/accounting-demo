export type TransactionType = 'income' | 'expense';

export interface TransactionCreate {
    amount: number;
    type: TransactionType;
    description: string;
}

export interface Transaction extends TransactionCreate {
    id: number;
    created_at: string;
    updated_at: string | null;
}

export interface Statistics {
    total_income: number;
    total_expense: number;
    net_amount: number;
    period_days: number;
}