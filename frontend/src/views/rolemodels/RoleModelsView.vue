<script setup>
import {ref,onMounted} from "vue"
import RoleModelCard from "../../components/RoleModelCard.vue"
import {getRoleModels} from "../../services/api"
const roleModels=ref([])
onMounted(async()=>{
  roleModels.value=await getRoleModels()
  console.log(roleModels.value)
})
</script>
<template>
  <div>
    <h1>Women in Science</h1>
    <div v-if="roleModels.length===0">
      No profiles available.
    </div>
    <RoleModelCard v-for="model in roleModels"
    :key="model.id"
    :roleModel="model"
    />
  </div>
</template>