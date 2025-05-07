<template>
	<view class="publish-container">
		<view class="form-group">
			<view class="form-item">
				<text class="form-label">需求标题</text>
				<input class="form-input" v-model="formData.title" placeholder="请输入需求标题" maxlength="50" />
			</view>
			
			<view class="form-item">
				<text class="form-label">需求类型</text>
				<picker class="form-picker" @change="bindTypeChange" :value="typeIndex" :range="demandTypes">
					<view class="picker-text">{{demandTypes[typeIndex]}}</view>
				</picker>
			</view>
			
			<view class="form-item">
				<text class="form-label">服务区域</text>
				<picker class="form-picker" mode="region" @change="bindRegionChange" :value="formData.region">
					<view class="picker-text">{{formData.region[0]}} {{formData.region[1]}} {{formData.region[2]}}</view>
				</picker>
			</view>
			
			<view class="form-item">
				<text class="form-label">需求详情</text>
				<textarea class="form-textarea" v-model="formData.description" placeholder="请详细描述您的需求，包括具体要求、工作量、时间要求等" maxlength="1000" />
			</view>
			
			<view class="form-item">
				<text class="form-label">预算范围</text>
				<view class="budget-input">
					<input class="form-input" v-model="formData.budget" type="digit" placeholder="输入预算金额" />
					<text class="budget-unit">元</text>
				</view>
			</view>
			
			<view class="form-item">
				<text class="form-label">联系方式</text>
				<input class="form-input" v-model="formData.contact" placeholder="请输入您的联系方式" />
			</view>
			
			<view class="form-item">
				<text class="form-label">截止日期</text>
				<picker class="form-picker" mode="date" :start="startDate" :end="endDate" @change="bindDateChange" :value="formData.deadline">
					<view class="picker-text">{{formData.deadline}}</view>
				</picker>
			</view>
			
			<view class="form-item upload-section">
				<text class="form-label">上传相关图片（选填）</text>
				<view class="upload-area">
					<view class="upload-item" v-for="(item, index) in formData.images" :key="index" @tap="previewImage(index)">
						<image class="upload-image" :src="item" mode="aspectFill"></image>
						<text class="delete-icon" @tap.stop="deleteImage(index)">×</text>
					</view>
					<view class="upload-item add-item" @tap="chooseImage" v-if="formData.images.length < 6">
						<text class="add-icon">+</text>
					</view>
				</view>
			</view>
		</view>
		
		<view class="button-group">
			<button class="cancel-button" @tap="cancelPublish">取消</button>
			<button class="publish-button" @tap="submitDemand">发布需求</button>
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
			const today = `${year}-${month}-${day}`;
			
			return {
				formData: {
					title: '',
					type: '航拍服务',
					description: '',
					budget: '',
					contact: '',
					region: ['广东省', '广州市', '海珠区'],
					deadline: today,
					images: []
				},
				demandTypes: ['航拍服务', '测绘服务', '植保服务', '电力巡检', '设备租赁', '其他服务'],
				typeIndex: 0,
				startDate: today,
				endDate: `${year + 1}-${month}-${day}`
			}
		},
		onLoad() {
			// 加载用户信息，自动填充联系方式
			const userInfo = uni.getStorageSync('userInfo');
			if (userInfo) {
				const userData = JSON.parse(userInfo);
				if (userData.phone) {
					this.formData.contact = userData.phone;
				}
			}
		},
		methods: {
			bindTypeChange(e) {
				this.typeIndex = e.detail.value;
				this.formData.type = this.demandTypes[this.typeIndex];
			},
			bindRegionChange(e) {
				this.formData.region = e.detail.value;
			},
			bindDateChange(e) {
				this.formData.deadline = e.detail.value;
			},
			chooseImage() {
				uni.chooseImage({
					count: 6 - this.formData.images.length,
					sizeType: ['compressed'],
					sourceType: ['album', 'camera'],
					success: (res) => {
						this.formData.images = [...this.formData.images, ...res.tempFilePaths];
					}
				});
			},
			previewImage(index) {
				uni.previewImage({
					current: this.formData.images[index],
					urls: this.formData.images
				});
			},
			deleteImage(index) {
				this.formData.images.splice(index, 1);
			},
			validateForm() {
				if (!this.formData.title.trim()) {
					uni.showToast({
						title: '请输入需求标题',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.description.trim()) {
					uni.showToast({
						title: '请输入需求详情',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.budget) {
					uni.showToast({
						title: '请输入预算范围',
						icon: 'none'
					});
					return false;
				}
				
				if (!this.formData.contact.trim()) {
					uni.showToast({
						title: '请输入联系方式',
						icon: 'none'
					});
					return false;
				}
				
				return true;
			},
			submitDemand() {
				if (!this.validateForm()) return;
				
				// 显示提交中加载动画
				uni.showLoading({
					title: '发布中...'
				});
				
				// 模拟提交过程
				setTimeout(() => {
					uni.hideLoading();
					
					uni.showToast({
						title: '发布成功',
						icon: 'success'
					});
					
					// 延迟跳转回需求列表页
					setTimeout(() => {
						uni.navigateBack();
					}, 1500);
				}, 2000);
			},
			cancelPublish() {
				uni.navigateBack();
			}
		}
	}
</script>

<style>
	.publish-container {
		padding: 30rpx;
		background-color: #f5f5f5;
	}
	
	.form-group {
		background-color: #fff;
		border-radius: 12rpx;
		padding: 20rpx 30rpx;
		margin-bottom: 30rpx;
	}
	
	.form-item {
		padding: 20rpx 0;
		border-bottom: 1px solid #eee;
	}
	
	.form-item:last-child {
		border-bottom: none;
	}
	
	.form-label {
		display: block;
		font-size: 28rpx;
		color: #333;
		margin-bottom: 20rpx;
		font-weight: bold;
	}
	
	.form-input {
		width: 100%;
		height: 80rpx;
		font-size: 28rpx;
		padding: 0 20rpx;
		background-color: #f9f9f9;
		border-radius: 6rpx;
	}
	
	.form-textarea {
		width: 100%;
		height: 240rpx;
		font-size: 28rpx;
		padding: 20rpx;
		background-color: #f9f9f9;
		border-radius: 6rpx;
	}
	
	.form-picker {
		width: 100%;
	}
	
	.picker-text {
		width: 100%;
		height: 80rpx;
		line-height: 80rpx;
		padding: 0 20rpx;
		background-color: #f9f9f9;
		border-radius: 6rpx;
		font-size: 28rpx;
	}
	
	.budget-input {
		display: flex;
		align-items: center;
	}
	
	.budget-unit {
		margin-left: 20rpx;
		font-size: 28rpx;
		color: #333;
	}
	
	.upload-area {
		display: flex;
		flex-wrap: wrap;
		margin: 0 -10rpx;
	}
	
	.upload-item {
		width: 210rpx;
		height: 210rpx;
		margin: 10rpx;
		position: relative;
		background-color: #f9f9f9;
		border-radius: 6rpx;
	}
	
	.upload-image {
		width: 100%;
		height: 100%;
		border-radius: 6rpx;
	}
	
	.add-item {
		display: flex;
		justify-content: center;
		align-items: center;
		border: 1px dashed #ddd;
	}
	
	.add-icon {
		font-size: 60rpx;
		color: #999;
	}
	
	.delete-icon {
		position: absolute;
		top: -20rpx;
		right: -20rpx;
		width: 40rpx;
		height: 40rpx;
		line-height: 36rpx;
		text-align: center;
		background-color: rgba(0, 0, 0, 0.5);
		color: #fff;
		border-radius: 50%;
		font-size: 30rpx;
	}
	
	.button-group {
		display: flex;
		justify-content: space-between;
	}
	
	.publish-button, .cancel-button {
		width: 45%;
		height: 90rpx;
		line-height: 90rpx;
		border-radius: 45rpx;
		font-size: 32rpx;
		font-weight: bold;
	}
	
	.publish-button {
		background-color: #007AFF;
		color: #fff;
	}
	
	.cancel-button {
		background-color: #f5f5f5;
		color: #666;
		border: 1px solid #ddd;
	}
</style> 