<template>
    <div class="card">
        <h2>
            {{roleModel.first_name}}
            {{roleModel.last_name}}
        </h2>
        <p>{{roleModel.stem_field}}</p>
        <p>{{roleModel.institution}}</p>
    </div>

</template>

<script setup>
define Props({
    roleModel:Object
})
</script>