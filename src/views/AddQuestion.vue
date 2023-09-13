<template>
    <div class="container">
        <div v-for="(qform, index) in forms" :key="index" class="form-container">
            <el-form :model="qform" label-width="120px" label-position="top">
                <el-form-item label="问题">
                    <el-input v-model="qform.question" class="input-field"></el-input>
                </el-form-item>
                <el-form-item label="选项">
                    <div v-for="(answer, aindex) in qform.answers" :key="aindex" class="answer-container">
                        <el-input v-model="answer.text" class="input-field"></el-input>
                        <el-button @click="removeAnswer(index, aindex)" class="remove-button">移除</el-button>
                    </div>
                    <el-button @click="addAnswer(index)" class="add-button">添加答案</el-button>
                </el-form-item>
                <el-form-item label="正确答案">
                    <el-select v-model="qform.rightanswer">
                        <el-option v-for="(answer, aindex) in qform.answers" :key="aindex" :label="answer.label"
                            :value="answer.label">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <el-button @click="removeForm(index)" type="danger">移除问题</el-button>
        </div>
        <el-row>
            <el-button @click="addForm" type="success" class="submit-button" >添加问题</el-button>
            <el-button type="primary" @click="submitForms" class="submit-button" >提交所有</el-button>
            <el-button type="primary" @click="DeleteForms" class="submit-button" >删除所有</el-button>
        </el-row>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { addRecord, getRecords, DeleteRecord, DeleteRecordById } from '../api/index';  // 替换为你的 api.js 路径
const forms = ref([
    {
        id: 1,
        question: '',
        answers: [{ text: '', label: 'A' }],
        rightanswer: 'A'
    }
]);

const labelGenerator = (index) => String.fromCharCode(65 + index);  // 从 ASCII 值生成 A, B, C, ...

const refreshLabels = (answers) => {
    answers.forEach((answer, index) => {
        answer.label = labelGenerator(index);
    });
};

watch(forms, (newForms) => {
    newForms.forEach(form => {
        refreshLabels(form.answers);
    });
}, { deep: true });

const addForm = () => {
    const newId = forms.value.length ? Math.max(forms.value.map(f => f.id)) + 1 : 1;
    forms.value.push({ id: newId, question: '', answers: [{ text: '', label: 'A' }] });
};

const removeForm = async (index) => {
    // 获取要删除的表单的ID
    const formId = forms.value[index].id;

    // 调用API以在服务器上删除记录
    const response = await DeleteRecordById(formId);

    if (response && response.status === 'success') {
        // 在客户端删除表单
        forms.value.splice(index, 1);
        ElMessage({
            message:`成功删除问题`,
            type: 'success',
        })
    } else {
        ElMessage.error('删除失败')
    }
};


const addAnswer = (formIndex) => {
    forms.value[formIndex].answers.push({ text: '' });
    refreshLabels(forms.value[formIndex].answers);
};

const removeAnswer = (formIndex, answerIndex) => {
    forms.value[formIndex].answers.splice(answerIndex, 1);
    refreshLabels(forms.value[formIndex].answers);
};

const submitForms = async () => {
    const result = await addRecord(forms.value);
    if (result && result.status === 'success') {
        ElMessage({
            message: '提交成功',
            type: 'success',
        })
    } else {
        ElMessage.error('提交失败')
    }
};
const DeleteForms = async () => {
    const result = await DeleteRecord(forms.value);
    if (result && result.status === 'success') {
        ElMessage({
            message: '删除成功',
            type: 'success',
        })
    } else {
        ElMessage.error('删除失败')
    }
};
onMounted(async () => {
    const data = await getRecords();
    if (data) {
        forms.value = data;
    }
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
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
