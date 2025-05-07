<template>
  <view class="demand-container">
    <view class="tab-container">
      <view class="tab-item" :class="{ active: activeTab === 'single' }" @click="switchTab('single')">
        <text>下单</text>
      </view>
      <view class="tab-item" :class="{ active: activeTab === 'combo' }" @click="switchTab('combo')">
        <text>多飞手组合下单</text>
      </view>
    </view>
    
    <!-- 单个需求发布 -->
    <view v-if="activeTab === 'single'" class="form-container">
      <view class="card">
        <view class="form-group">
          <text class="form-label">需求标题</text>
          <input class="form-input" type="text" v-model="formData.title" placeholder="请简要描述您的需求" />
        </view>
        
        <view class="form-group">
          <text class="form-label">需求类型</text>
          <picker mode="selector" :range="demandTypes" @change="handleTypeChange">
            <view class="picker-view">
              <text>{{ demandTypes[formData.typeIndex] || '请选择需求类型' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">飞行区域</text>
          <picker mode="region" @change="handleRegionChange">
            <view class="picker-view">
              <text>{{ formData.region.join(' ') || '请选择区域' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">详细地址</text>
          <input class="form-input" type="text" v-model="formData.address" placeholder="请输入详细地址" />
        </view>
        
        <view class="form-group">
          <text class="form-label">预算范围</text>
          <picker mode="selector" :range="budgetRanges" @change="handleBudgetChange">
            <view class="picker-view">
              <text>{{ budgetRanges[formData.budgetIndex] || '请选择预算范围' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">期望完成日期</text>
          <picker mode="date" :start="minDate" @change="handleDateChange">
            <view class="picker-view">
              <text>{{ formData.expectDate || '请选择日期' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">需求详情</text>
          <textarea class="form-textarea" v-model="formData.description" placeholder="请详细描述您的需求，例如：需要什么服务，对设备有什么要求等"></textarea>
        </view>
        
        <view class="form-group">
          <text class="form-label">联系方式</text>
          <input class="form-input" type="text" v-model="formData.contact" placeholder="请留下您的手机号或微信" />
        </view>
        
        <view class="upload-section">
          <text class="form-label">上传附件</text>
          <view class="upload-list">
            <view class="upload-item" v-for="(item, index) in formData.attachments" :key="index">
              <image class="upload-image" :src="item" mode="aspectFill"></image>
              <text class="delete-icon" @click="deleteAttachment(index)">×</text>
            </view>
            <view class="upload-add" @click="chooseImage" v-if="formData.attachments.length < 9">
              <text class="add-icon">+</text>
              <text class="add-text">添加图片</text>
            </view>
          </view>
        </view>
      </view>
      
      <button class="submit-btn" @click="submitDemand">发布需求</button>
    </view>
    
    <!-- 多飞手组合下单 -->
    <view v-else class="form-container">
      <view class="card">
        <view class="form-group">
          <text class="form-label">项目名称</text>
          <input class="form-input" type="text" v-model="comboData.title" placeholder="请输入项目名称" />
        </view>
        
        <view class="form-group">
          <text class="form-label">项目类型</text>
          <picker mode="selector" :range="projectTypes" @change="handleProjectTypeChange">
            <view class="picker-view">
              <text>{{ projectTypes[comboData.typeIndex] || '请选择项目类型' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">项目区域</text>
          <picker mode="region" @change="handleComboRegionChange">
            <view class="picker-view">
              <text>{{ comboData.region.join(' ') || '请选择区域' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">项目周期</text>
          <picker mode="selector" :range="projectDurations" @change="handleDurationChange">
            <view class="picker-view">
              <text>{{ projectDurations[comboData.durationIndex] || '请选择项目周期' }}</text>
              <text class="iconfont icon-right"></text>
            </view>
          </picker>
        </view>
        
        <view class="form-group">
          <text class="form-label">总预算</text>
          <input class="form-input" type="digit" v-model="comboData.budget" placeholder="请输入总预算(元)" />
        </view>
        
        <view class="form-group">
          <text class="form-label">项目描述</text>
          <textarea class="form-textarea" v-model="comboData.description" placeholder="请详细描述项目情况，包括需要多少飞手、设备要求、服务内容等"></textarea>
        </view>
        
        <view class="sub-title">团队需求</view>
        
        <view class="team-req-list">
          <view class="team-req-item" v-for="(item, index) in comboData.teamRequirements" :key="index">
            <view class="team-req-header">
              <text class="team-req-title">需求{{index+1}}: {{item.type}}</text>
              <text class="team-req-delete" @click="deleteTeamReq(index)">删除</text>
            </view>
            <view class="team-req-content">
              <text>人数: {{item.count}}人</text>
              <text>技能要求: {{item.skills}}</text>
            </view>
          </view>
          
          <view class="add-team-req" @click="showAddTeamReqModal">
            <text class="add-team-icon">+</text>
            <text>添加团队需求</text>
          </view>
        </view>
      </view>
      
      <button class="submit-btn" @click="submitComboRequest">发布组合需求</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    
    return {
      activeTab: 'single',
      minDate: `${year}-${month}-${day}`,
      demandTypes: ['航拍服务', '植保作业', '巡检服务', '3D建模', '设备采购', '其他服务'],
      budgetRanges: ['1000以下', '1000-3000', '3000-5000', '5000-10000', '10000以上'],
      projectTypes: ['影视拍摄', '农业植保', '工程巡检', '大型活动', '测绘建模', '其他项目'],
      projectDurations: ['3天内', '1周内', '2周内', '1个月内', '1-3个月', '3个月以上'],
      
      formData: {
        title: '',
        typeIndex: 0,
        region: [],
        address: '',
        budgetIndex: 0,
        expectDate: '',
        description: '',
        contact: '',
        attachments: []
      },
      
      comboData: {
        title: '',
        typeIndex: 0,
        region: [],
        durationIndex: 0,
        budget: '',
        description: '',
        teamRequirements: []
      }
    }
  },
  methods: {
    switchTab(tab) {
      this.activeTab = tab;
    },
    
    handleTypeChange(e) {
      this.formData.typeIndex = e.detail.value;
    },
    
    handleRegionChange(e) {
      this.formData.region = e.detail.value;
    },
    
    handleBudgetChange(e) {
      this.formData.budgetIndex = e.detail.value;
    },
    
    handleDateChange(e) {
      this.formData.expectDate = e.detail.value;
    },
    
    chooseImage() {
      uni.chooseImage({
        count: 9 - this.formData.attachments.length,
        success: (res) => {
          this.formData.attachments = [...this.formData.attachments, ...res.tempFilePaths];
        }
      });
    },
    
    deleteAttachment(index) {
      this.formData.attachments.splice(index, 1);
    },
    
    submitDemand() {
      // 表单验证
      if (!this.formData.title) {
        uni.showToast({
          title: '请输入需求标题',
          icon: 'none'
        });
        return;
      }
      
      if (this.formData.region.length === 0) {
        uni.showToast({
          title: '请选择飞行区域',
          icon: 'none'
        });
        return;
      }
      
      if (!this.formData.description) {
        uni.showToast({
          title: '请填写需求详情',
          icon: 'none'
        });
        return;
      }
      
      if (!this.formData.contact) {
        uni.showToast({
          title: '请填写联系方式',
          icon: 'none'
        });
        return;
      }
      
      // 提交表单数据
      uni.showLoading({
        title: '正在提交...'
      });
      
      // 模拟API调用
      setTimeout(() => {
        uni.hideLoading();
        
        // 跳转到服务类型选择页
        uni.navigateTo({
          url: '/pages/demand/service-select'
        });
      }, 1500);
      
      // 实际项目中的API调用
      // this.$request({
      //   url: '/demand/create',
      //   method: 'POST',
      //   data: {
      //     title: this.formData.title,
      //     type: this.demandTypes[this.formData.typeIndex],
      //     region: this.formData.region.join(' '),
      //     address: this.formData.address,
      //     budget: this.budgetRanges[this.formData.budgetIndex],
      //     expectDate: this.formData.expectDate,
      //     description: this.formData.description,
      //     contact: this.formData.contact,
      //     attachments: this.formData.attachments
      //   }
      // }).then(res => {
      //   uni.hideLoading();
      //   uni.showToast({
      //     title: '发布成功',
      //     icon: 'success'
      //   });
      //   
      //   // 跳转到服务类型选择页
      //   uni.navigateTo({
      //     url: '/pages/demand/service-select'
      //   });
      // }).catch(err => {
      //   uni.hideLoading();
      //   uni.showToast({
      //     title: '发布失败，请重试',
      //     icon: 'none'
      //   });
      // });
    },
    
    handleProjectTypeChange(e) {
      this.comboData.typeIndex = e.detail.value;
    },
    
    handleComboRegionChange(e) {
      this.comboData.region = e.detail.value;
    },
    
    handleDurationChange(e) {
      this.comboData.durationIndex = e.detail.value;
    },
    
    showAddTeamReqModal() {
      // 实际项目中可以使用Modal组件或自定义弹窗
      // 这里简化处理，直接添加一个示例需求
      this.comboData.teamRequirements.push({
        type: '无人机飞手',
        count: 2,
        skills: '熟练操作大疆经纬系列无人机，有3年以上航拍经验'
      });
    },
    
    deleteTeamReq(index) {
      this.comboData.teamRequirements.splice(index, 1);
    },
    
    submitComboRequest() {
      // 表单验证
      if (!this.comboData.title) {
        uni.showToast({
          title: '请输入项目名称',
          icon: 'none'
        });
        return;
      }
      
      if (this.comboData.region.length === 0) {
        uni.showToast({
          title: '请选择项目区域',
          icon: 'none'
        });
        return;
      }
      
      if (!this.comboData.budget) {
        uni.showToast({
          title: '请填写项目预算',
          icon: 'none'
        });
        return;
      }
      
      if (!this.comboData.description) {
        uni.showToast({
          title: '请填写项目描述',
          icon: 'none'
        });
        return;
      }
      
      if (this.comboData.teamRequirements.length === 0) {
        uni.showToast({
          title: '请添加至少一个团队需求',
          icon: 'none'
        });
        return;
      }
      
      // 提交表单数据
      uni.showLoading({
        title: '正在提交...'
      });
      
      // 模拟API调用
      setTimeout(() => {
        uni.hideLoading();
        uni.showToast({
          title: '发布成功',
          icon: 'success'
        });
        
        // 跳转到组合套餐选择页
        uni.navigateTo({
          url: '/pages/demand/combo-package'
        });
      }, 1500);
    }
  }
}
</script>

<style>
.demand-container {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 30rpx;
}

.tab-container {
  display: flex;
  background-color: #fff;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 10;
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  position: relative;
  font-size: 28rpx;
}

.tab-item.active {
  color: #007AFF;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: 60rpx;
  height: 4rpx;
  background-color: #007AFF;
  border-radius: 2rpx;
}

.form-container {
  padding: 20rpx;
}

.card {
  background-color: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.form-group {
  margin-bottom: 24rpx;
}

.form-label {
  display: block;
  margin-bottom: 10rpx;
  font-size: 28rpx;
  font-weight: 500;
}

.form-input {
  width: 100%;
  height: 80rpx;
  border: 1px solid #eee;
  border-radius: 8rpx;
  padding: 0 20rpx;
  box-sizing: border-box;
  font-size: 28rpx;
}

.form-textarea {
  width: 100%;
  height: 200rpx;
  border: 1px solid #eee;
  border-radius: 8rpx;
  padding: 20rpx;
  box-sizing: border-box;
  font-size: 28rpx;
}

.picker-view {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 80rpx;
  border: 1px solid #eee;
  border-radius: 8rpx;
  padding: 0 20rpx;
  box-sizing: border-box;
  font-size: 28rpx;
}

.upload-section {
  margin-top: 30rpx;
}

.upload-list {
  display: flex;
  flex-wrap: wrap;
  margin-top: 10rpx;
}

.upload-item {
  width: 160rpx;
  height: 160rpx;
  margin-right: 20rpx;
  margin-bottom: 20rpx;
  position: relative;
}

.upload-image {
  width: 100%;
  height: 100%;
  border-radius: 8rpx;
}

.delete-icon {
  position: absolute;
  top: -16rpx;
  right: -16rpx;
  width: 40rpx;
  height: 40rpx;
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26rpx;
  z-index: 1;
}

.upload-add {
  width: 160rpx;
  height: 160rpx;
  border: 1px dashed #ccc;
  border-radius: 8rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.add-icon {
  font-size: 48rpx;
  color: #999;
  margin-bottom: 10rpx;
}

.add-text {
  font-size: 24rpx;
  color: #999;
}

.submit-btn {
  width: 90%;
  height: 90rpx;
  line-height: 90rpx;
  background-color: #007AFF;
  color: #fff;
  font-size: 32rpx;
  border-radius: 45rpx;
  margin: 40rpx auto;
}

.sub-title {
  font-size: 30rpx;
  font-weight: bold;
  margin: 30rpx 0 20rpx;
  position: relative;
  padding-left: 20rpx;
}

.sub-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 6rpx;
  height: 30rpx;
  width: 6rpx;
  background-color: #007AFF;
  border-radius: 3rpx;
}

.team-req-list {
  margin-top: 20rpx;
}

.team-req-item {
  background-color: #f8f8f8;
  border-radius: 8rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
}

.team-req-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10rpx;
}

.team-req-title {
  font-size: 28rpx;
  font-weight: 500;
}

.team-req-delete {
  color: #ff4d4f;
  font-size: 26rpx;
}

.team-req-content {
  display: flex;
  flex-direction: column;
  font-size: 26rpx;
  color: #666;
}

.team-req-content text {
  margin-bottom: 6rpx;
}

.add-team-req {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 90rpx;
  background-color: #f8f8f8;
  border-radius: 8rpx;
  color: #007AFF;
  font-size: 28rpx;
}

.add-team-icon {
  margin-right: 10rpx;
  font-size: 32rpx;
}
</style> 