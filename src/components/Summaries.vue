<script setup>
const emit = defineEmits(["toggleSummaries"]);
const toggleSummaries = () => {
    emit("toggleSummaries");
};
</script>

<template>
        <div class="flex justify-center items-center w-full h-full absolute top-0">
            <div class="w-[50%] h-[50vh] bg-(--md-sys-color-surface) rounded-[12px] border border-(--md-sys-color-outline-variant) p-4">
                <div class="flex justify-end">
                    <md-icon-button @click="toggleSummaries">
                        <md-icon>close</md-icon>
                    </md-icon-button>
                </div>

                <div class="flex flex-col text-justify w-[90%] m-auto gap-10 items-center justify-center h-[80%]">
                    <span class="text-3xl text-center">Summary Header</span>
                    <span>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed rutrum ligula. Duis massa diam, mollis vel vehicula at, tempor et urna. Maecenas eget mi tortor. Maecenas a vehicula lorem. Sed vel lacus sed ligula facilisis auctor. Maecenas eu nunc vestibulum, molestie eros in, fermentum sem. Sed hendrerit massa dui, at vehicula felis convallis vitae. Nulla facilisi. Maecenas cursus finibus urna non accumsan. Aliquam vehicula lacus eget congue lobortis. Nam velit enim, fermentum ac eros sit amet, iaculis tincidunt risus. Fusce lacinia rhoncus quam. Sed hendrerit pharetra nulla, et iaculis neque eleifend ut. Phasellus vitae egestas felis. Morbi libero arcu, mattis sed ante id, luctus accumsan lectus. Nullam sagittis, risus vel lobortis venenatis, urna sem pellentesque ipsum, in dignissim dolor tortor vel urna. In rutrum ligula non scelerisque cursus. Nunc laoreet diam lacus, vel volutpat neque iaculis at. Mauris sit amet vestibulum arcu. In ullamcorper risus in faucibus ullamcorper. Donec eu venenatis nulla. Etiam eu mattis nisi, sed pulvinar elit. Vestibulum placerat justo ac est sagittis finibus. Etiam congue, lacus tristique fringilla semper, sem sem elementum ligula, quis dignissim odio ipsum nec mi. Nam sodales mollis rutrum. Aenean condimentum lorem vitae dapibus blandit. Nam eget leo in est aliquam mattis. Nulla porttitor lacinia dolor, sit amet pellentesque ante porttitor et. Pellentesque nec est consequat, laoreet risus id, maximus ex. Pellentesque mollis eu ante molestie scelerisque. Duis finibus felis est, non sodales magna vestibulum nec. Fusce massa ante, interdum nec elementum at, vehicula in metus. Duis et neque rutrum, commodo ex non, condimentum nisi. Quisque erat nunc, rhoncus id elementum commodo, elementum eget libero.</span>
                </div>
            </div>
        </div>
</template>