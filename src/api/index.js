import axios from 'axios';
const apiUrl = import.meta.env.VITE_API_BASE_URL;
const api = axios.create({
    baseURL: apiUrl,
    headers: {
        'Content-Type': 'application/json',
    },
});
export const addRecord = async (forms) => {
    try {
        const response = await api.post('/add', {
            forms,
        });
        return response.data;
    } catch (error) {
        console.error('添加记录时出错:', error);
        return null;
    }
};
export const evaluator= async (forms) => {
    try {
        const response = await api.post('/evaluator', {
            forms,
        });
        return response.data;
    } catch (error) {
        console.error('添加记录时出错:', error);
        return null;
    }
};
export const DeleteRecord = async () => {
    try {
        const response = await api.get('/deleteall', {
        });
        return response.data
    } catch (error) {
        console.error('添加记录时出错:', error);
        return null;
    }
};
export const DeleteRecordById = async (id) => {
    try {
        const response = await api.post('/deletebyid', { id: id });
        return response.data;
    } catch (error) {
        console.error('删除记录时出错:', error);
        return null;
    }
};

export const getRecords = async () => {
    try {
        const response = await api.get('/getrecords');
        if (response.data.status === 'success') {
            return response.data.data;
        }
    } catch (error) {
        console.error('获取记录时出错:', error);
    }
    return null; // or some default value
};


export const getevaluatrecords = async () => {
    try {
        const response = await api.get('/getevaluatrecords');
        if (response.data.status === 'success') {
            console.log(response.data.data)
            return response.data.data;
        }
    } catch (error) {
        console.error('获取记录时出错:', error);
    }
    return null; // or some default value
};

export const DeletevaById = async (id) => {
    try {
        const response = await api.post('/delete_evaluation_result', { _id: id });
        return response.data;
    } catch (error) {
        console.error('删除记录时出错:', error);
        return null;
    }
};
