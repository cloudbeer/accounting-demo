<template>
    <div class="home">
        <!-- 统计卡片 -->
        <van-card class="statistics-card">
            <template #title>
                <div class="statistics-title">{{ dayjs().format('YYYY年MM月') }}统计</div>
            </template>
            <template #desc>
                <div class="statistics-content">
                    <div class="stat-item">
                        <span class="label">收入</span>
                        <span class="amount income">¥{{ statistics.total_income.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">支出</span>
                        <span class="amount expense">¥{{ statistics.total_expense.toFixed(2) }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="label">结余</span>
                        <span class="amount" :class="statistics.net_amount >= 0 ? 'income' : 'expense'">
                            ¥{{ statistics.net_amount.toFixed(2) }}
                        </span>
                    </div>
                </div>
            </template>
        </van-card>

        <!-- 交易列表 -->
        <van-list v-model:loading="loading" :finished="finished" finished-text="没有更多了" @load="loadTransactions">
            <van-cell-group inset>
                <van-swipe-cell v-for="item in transactions" :key="item.id">
                    <van-cell>
                        <template #title>
                            <div class="transaction-title">
                                <span>{{ item.description }}</span>
                                <span :class="item.type === 'income' ? 'income' : 'expense'">
                                    {{ item.type === 'income' ? '+' : '-' }}¥{{ item.amount.toFixed(2) }}
                                </span>
                            </div>
                        </template>
                        <template #label>
                            <span class="transaction-time">{{ dayjs(item.created_at).format('YYYY-MM-DD HH:mm')
                                }}</span>
                        </template>
                    </van-cell>
                    <template #right>
                        <van-button square type="danger" text="删除" @click="deleteItem(item.id)" />
                    </template>
                </van-swipe-cell>
            </van-cell-group>
        </van-list>

        <!-- 添加按钮 -->
        <van-button round type="primary" class="add-button" icon="plus" @click="showAddDialog = true">
            记一笔
        </van-button>

        <!-- 添加交易对话框 -->
        <van-dialog v-model:show="showAddDialog" title="记一笔" show-cancel-button @confirm="handleAdd">
            <van-cell-group inset>
                <van-field v-model="newTransaction.text" label="描述" placeholder="例如：今天买菜花了50元" type="textarea" rows="3"
                    autosize />
            </van-cell-group>
        </van-dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { showToast, showLoadingToast } from 'vant';
import dayjs from 'dayjs';
import type { Transaction } from '../types';
import { getTransactions, createTransactionFromText, deleteTransaction, getStatistics } from '../services/api';

const transactions = ref<Transaction[]>([]);
const loading = ref(false);
const finished = ref(false);
const showAddDialog = ref(false);
const statistics = ref({
    total_income: 0,
    total_expense: 0,
    net_amount: 0,
    period_days: 30
});

const newTransaction = ref({
    text: ''
});

// 加载交易记录
const loadTransactions = async () => {
    try {
        loading.value = true;
        const data = await getTransactions();
        transactions.value = data;
        finished.value = true;
    } catch (error) {
        showToast('加载失败');
    } finally {
        loading.value = false;
    }
};

// 加载统计数据
const loadStatistics = async () => {
    try {
        const data = await getStatistics();
        statistics.value = data;
    } catch (error) {
        showToast('统计数据加载失败');
    }
};

// 添加新交易
const handleAdd = async () => {
    if (!newTransaction.value.text) {
        showToast('请输入交易描述');
        return;
    }

    const loading = showLoadingToast({
        message: '正在处理...',
        forbidClick: true,
    });

    try {
        await createTransactionFromText(newTransaction.value.text);
        showToast('添加成功');
        newTransaction.value.text = '';
        loadTransactions();
        loadStatistics();
    } catch (error) {
        showToast('添加失败');
    } finally {
        loading.close();
    }
};

// 删除交易
const deleteItem = async (id: number) => {
    try {
        await deleteTransaction(id);
        showToast('删除成功');
        loadTransactions();
        loadStatistics();
    } catch (error) {
        showToast('删除失败');
    }
};

onMounted(() => {
    loadTransactions();
    loadStatistics();
});
</script>

<style scoped>
.home {
    padding-bottom: 80px;
}

.statistics-card {
    margin: 16px;
    background-color: #fff;
}

.statistics-title {
    font-size: 16px;
    font-weight: bold;
}

.statistics-content {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
}

.stat-item {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.label {
    font-size: 14px;
    color: #666;
}

.amount {
    font-size: 16px;
    font-weight: bold;
    margin-top: 4px;
}

.income {
    color: #07c160;
}

.expense {
    color: #ee0a24;
}

.transaction-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.transaction-time {
    font-size: 12px;
    color: #999;
}

.add-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 999;
}
</style>