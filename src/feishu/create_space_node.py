import json

import lark_oapi as lark
from lark_oapi.api.wiki.v2 import *


# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
def main():
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder() \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    
    ### 添加内容需要通过创建块：使用obj_token作为路径参数，传入CreateDocumentBlockChildren
    request: CreateSpaceNodeRequest = CreateSpaceNodeRequest.builder() \
        .space_id("7469611678926602241") \
        .request_body(Node.builder()
            .obj_type("docx")
            .node_type("origin")
            .title("test")
            .build()) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-emF6Jaaq92XXhkLCTWt_CrklmN1005nxiww04gu02HrF").build()
    response: CreateSpaceNodeResponse = client.wiki.v2.space_node.create(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()