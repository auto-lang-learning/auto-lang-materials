import json

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *


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
    request: CreateDocumentBlockChildrenRequest = CreateDocumentBlockChildrenRequest.builder() \
        .document_id("UipGds3OBoenUZx986LccZpunbb") \
        .block_id("UipGds3OBoenUZx986LccZpunbb") \
        .document_revision_id(-1) \
        .request_body(CreateDocumentBlockChildrenRequestBody.builder()
            .children([Block.builder()
                .block_type(2)
                .text(Text.builder()
                    .style(TextStyle.builder()
                        .build())
                    .elements([TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("多人实时协同，插入一切元素。不仅是在线文档，更是")
                            .text_element_style(TextElementStyle.builder()
                                .background_color(14)
                                .text_color(5)
                                .build())
                            .build())
                        .build(), 
                        TextElement.builder()
                        .text_run(TextRun.builder()
                            .content("强大的创作和互动工具")
                            .text_element_style(TextElementStyle.builder()
                                .bold(True)
                                .background_color(14)
                                .text_color(5)
                                .build())
                            .build())
                        .build()
                        ])
                    .build())
                .build()
                ])
            .index(0)
            .build()) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-emF6Jaaq92XXhkLCTWt_CrklmN1005nxiww04gu02HrF").build()
    response: CreateDocumentBlockChildrenResponse = client.docx.v1.document_block_children.create(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.docx.v1.document_block_children.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()