<template>
    <div class="container">
        <el-form :model="evaluatorInfo" label-width="120px" label-position="top">
            <el-form-item label="评测人">
                <el-input v-model="evaluatorInfo.name" class="input-field"></el-input>
            </el-form-item>
        </el-form>
        <div v-for="(qform, index) in forms" :key="index" class="form-container">
            <el-form :model="qform" label-width="120px" label-position="top">
                <el-form-item label="问题">
                    <el-input v-model="qform.question" class="input-field"></el-input>
                </el-form-item>
                <el-form-item label="选项">
                    <el-radio-group v-model="qform.rightanswer">
                        <el-radio v-for="(answer, aindex) in qform.answers" :key="aindex" :label="answer.label">
                            {{ answer.label }} {{ answer.text }}
                        </el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="选择答案">
                    <el-select v-model="qform.rightanswer">
                        <el-option v-for="(answer, aindex) in qform.answers" :key="aindex" :label="answer.label"
                            :value="answer.label">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
        </div>
        <el-row>
            <el-button type="primary" @click="submitForms" class="submit-button" icon="el-icon-upload">保存评测表</el-button>
            <el-button type="primary" @click="submitForms" class="submit-button" icon="el-icon-upload">提交评测</el-button>
        </el-row>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { evaluator, getRecords } from '../api/index';  // 替换为你的 api.js 路径
const forms = ref([
    {
        id: 1,
        question: '',
        answers: [{ text: '', label: 'A' }],
        rightanswer: 'A'
    }
]);
const evaluatorInfo = ref({
    name: ''  // 评测人姓名
});
const labelGenerator = (index) => String.fromCharCode(65 + index);  // 从 ASCII 值生成 A, B, C, ...

const refreshLabels = (answers) => {
    answers.forEach((answer, index) => {
        answer.label = labelGenerator(index);
    });
};

watch(forms, (newForms) => {
    newForms.forEach(form => {
        refreshLabels(form.answers);
        console.log(form.id, form.rightanswer);
    });
}, { deep: true });


const submitForms = async () => {
    // 构建一个包含问题ID和选择的答案的数据对象
    const formData = {
        evaluator: evaluatorInfo.value.name, // 添加评测人的姓名
        questions: forms.value.map(form => ({
            id: form.id,  // 问题ID
            answer: form.rightanswer  // 选择的答案
        }))
    };
    const result = await evaluator(formData);
    if (result && result.status === 'success') {
        ElMessage({
            message: '已提交评测',
            type: 'success',
        })
    } else {
        ElMessage.error('提交评测表单失败')
    }
};
onMounted(async () => {
    const data = await getRecords();
    if (data) {
        forms.value = data;
    }
    forms.value.forEach(form => {
        form.rightanswer = '';  // 或者设置为 null，取决于你的需求
    });
});
</script>


<style scoped>
.container {
    max-width: 1000px;
    margin: auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    border-radius: 15px;
}

.form-container {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #e8e8e8;
    border-radius: 10px;
}

.input-field {
    width: 70%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.answer-container {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.remove-button,
.add-button,
.submit-button {
    margin-top: 10px;
    margin-right: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
