import {reactive, readonly} from "vue";

const currentUser = reactive({
    role: ""
})

const setCurrentUser = (role) => {
    currentUser.role = role
}

export const globalStateStore = () => {
    currentUser: readonly(currentUser),
    setCurrentUser
}