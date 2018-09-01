# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

@summary: 功能开关装饰器，function_check（功能开关检测）
@usage：
          >>> from app_control.decorators import function_check
          >>> @function_check('test_func')
          >>> def test_func(request):
          >>>     pass
"""

from django.conf import settings

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs
from app_control.utils import func_check
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


def function_check(func_code):
    """
    功能开关装饰器
    @param func_code: 功能ID
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            _result, _message = func_check(func_code)
            if _result == 1:
                return view_func(request, *args, **kwargs)
            else:
                return _redirect_func_check_failed(request)
        return _wrapped_view
    return decorator


def _redirect_func_check_failed(request):
    """
    跳转功能权限检测失败的提示页面
    """
    url = '%saccount/check_failed/?code=func_check' % settings.SITE_URL
    if request.is_ajax():
        # ajax跳转页面，需要借助settings.js实现页面跳转或redirect跳转。
        resp = HttpResponse(status=402, content=url)
        return resp
    else:
        # 非ajax请求，则直接跳转页面
        return redirect(url)
