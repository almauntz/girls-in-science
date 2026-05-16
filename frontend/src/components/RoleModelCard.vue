<template>

    <div class="card">

        <h2>
            {{ roleModel.first_name }}
            {{ roleModel.last_name }}
        </h2>

        <p>{{ roleModel.stem_field }}</p>

        <p>{{ roleModel.institution }}</p>

    </div>

</template>

<script setup>

defineProps({
    roleModel: Object
})

</script>