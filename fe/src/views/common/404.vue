<template>
  <div class="main-body-div">
    <el-row>
      <el-col :span="24">
        <img src="@/assets/404.png" alt="" class="main-body-img" />
      </el-col>
      <el-col>
        <div>
            <p class="status-code">404</p>
            <p class="status-desc">你所訪問的頁面不存在...</p>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.main-body-img{
    margin-top: 150px;
}
.main-body-div{
    text-align: center;
    height: 100vh;
    width: 100vw;
}
.status-code{
    margin-top: 20px;
    margin-bottom: 10px;
    font-size: 95px;
    font-weight: bold;
    color: rgb(54,95,230);
}
.status-desc{
    color: rgb(145, 143, 143);
}
</style>