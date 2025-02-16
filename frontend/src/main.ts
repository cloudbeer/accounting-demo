import { createApp } from 'vue'
import {
    Button,
    List,
    Cell,
    CellGroup,
    Card,
    Dialog,
    Field,
    Toast,
    SwipeCell
} from 'vant';
import 'vant/lib/index.css';
import App from './App.vue'

const app = createApp(App)

// 注册Vant组件
app.use(Button)
    .use(List)
    .use(Cell)
    .use(CellGroup)
    .use(Card)
    .use(Dialog)
    .use(Field)
    .use(Toast)
    .use(SwipeCell)

app.mount('#app')
