import { axiosService } from '../../plugins/axios';

const ENDPOINT = '/shops/expenses/';

export const expensesService = {
    getExpenses(shopId, params = {}) {
        return axiosService.get(ENDPOINT, { params: { shop: shopId, ...params } });
    },
    getExpense(id) {
        return axiosService.get(`${ENDPOINT}${id}/`);
    },
    createExpense(data) {
        return axiosService.post(ENDPOINT, data);
    },
    updateExpense(id, data) {
        return axiosService.put(`${ENDPOINT}${id}/`, data);
    },
    deleteExpense(id) {
        return axiosService.delete(`${ENDPOINT}${id}/`);
    }
};
