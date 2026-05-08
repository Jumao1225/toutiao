from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRegisterRequest(BaseModel):
    username: str
    password: str


# user_info 对应的类: 基础类 + Info 类 （id，用户名）
class UserInfoBase(BaseModel):
    """
    用户信息基础类，包含可选的用户信息字段
    """
    nickname: Optional[str] = Field(None, max_length=50, description="用户昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="用户头像URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="用户性别，0-未知，1-男，2-女")
    bio: Optional[str] = Field(None, max_length=255, description="用户个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从 ORM 对象属性中取值
    )


# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True,  # alias / 字段名兼容 允许通过字段名称来填充数据
        from_attributes=True  # 允许从 ORM 对象属性中取值
    )


# 更新用户信息的模型类
class UserUpdateRequest(UserInfoBase):
    phone: Optional[str] = Field(None, max_length=20, description="用户手机号")


# 修改用户密码
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")
