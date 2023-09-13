<template>
    <div class="container">
        <el-select v-model="selectedResultIndex">
            <el-option
                v-for="(res, index) in allResults"
                :key="index"
                :label="res.evaluator + ' - ' + res.evaluation_time"
                :value="index">
            </el-option>
        </el-select>
        <div class="header">
            <h2>测评结果</h2>
            <p>评测员: {{ result.evaluator }}</p>
            <p>评测时间: {{ formattedTime }}</p>
            <p>得分: {{  totalScore }}</p>
        </div>
        <div v-for="(evaluation, index) in result.evaluation_results" :key="index" class="result-container">
            <div class="question">
                <strong>{{ evaluation.question_content }}</strong>
            </div>
            <div v-for="answer in evaluation.question_answers" :key="answer.label" class="answer">
                {{ answer.label }} : {{ answer.text }}
            </div>
            <div class="model-answer">
                评测员答案: {{ evaluation.model_answer }}
            </div>
            <div class="score">
                得分: {{ evaluation.score }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted,watch,computed} from 'vue';
import { getevaluatrecords } from '../api/index';  // 替换为你的 api.js 路径
const selectedResultIndex = ref(0);  // 新增：选中的评测结果的索引
const allResults = ref([]);  // 新增：所有的评测结果
const result = ref({});  // 用于存储当前选中的评测结果
const totalScore = computed(() => {
    if (result.value.evaluation_results && result.value.evaluation_results.length > 0) {
        const correctAnswers = result.value.evaluation_results.reduce((sum, current) => sum + current.score, 0);
        const totalQuestions = result.value.evaluation_results.length;
        return ((correctAnswers / totalQuestions) * 100).toFixed(2);  // 满分为 100 分
    }
    return 0;  // 如果没有评测结果，得分为 0
});
const formattedTime = computed(() => {
    if (result.value.evaluation_time) {
        const date = new Date(result.value.evaluation_time);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hour = date.getHours().toString().padStart(2, '0');
        const minute = date.getMinutes().toString().padStart(2, '0');
        return `${year}-${month}-${day} ${hour}:${minute}`;
    }
    return '';  // 如果没有评测时间，返回空字符串
});

onMounted(async () => {
    const data = await getevaluatrecords();
    if (data) {
        allResults.value = data;  // 设置所有的评测结果
        result.value = data[selectedResultIndex.value];  // 设置默认选中的评测结果
    }
});
// 新增：当选中的评测结果索引变化时，更新result
watch(selectedResultIndex, (newIndex) => {
    result.value = allResults.value[newIndex];
});
</script>

<style scoped>
.container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    border-radius: 15px;
}

.header {
    margin-bottom: 20px;
}

.result-container {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
}

.question {
    font-weight: bold;
    margin-bottom: 10px;
}

.answer {
    margin-bottom: 5px;
}

.model-answer,
.score {
    margin-top: 10px;
    font-weight: bold;
}
</style>
