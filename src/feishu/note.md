获取user_access_token的方法还需要再讨论，目前是手动从飞书API调试台获取，有效期两个小时


通过get_note_space获取wiki节点文档的id 
https://open.feishu.cn/api-explorer/cli_a720002cf32f100b?apiName=get_node&project=wiki&resource=space&version=v2


用list_doc_blocks获取文档里面所有块的内容
https://open.feishu.cn/api-explorer/cli_a720002cf32f100b?apiName=list&project=docx&resource=document.block&version=v1


用batch_update_doc_block批量更新文档块的内容
https://open.feishu.cn/api-explorer/cli_a720002cf32f100b?apiName=batch_update&project=docx&resource=document.block&version=v1





用create_space_node创建一个新的wiki节点文档
https://open.feishu.cn/api-explorer/cli_a720002cf32f100b?apiName=create&project=wiki&resource=space.node&version=v2


用create_doc_block_child在文档里面创建一个新的文档块
https://open.feishu.cn/api-explorer/cli_a720002cf32f100b?apiName=create&project=docx&resource=document.block.children&version=v1








有两种方法获取文档内容：
1. ListDocumentBlockRequest， 调试结果参考tes文件
2. GetDocumentBlockChildrenRequest， 调试结果参照tes2文件

第一种方法比第二种方法能够多获取以下信息，但是对于更新块的内容，似乎也没有什么帮助。需要研究一下到底用哪种方法
{
        "block_id": "UipGds3OBoenUZx986LccZpunbb",
        "block_type": 1,
        "children": [
          "doxcn2wKreT0oZBnBNLIRMAVi0f",
          "doxcn2z9cgnPQWNCB3Q1vNek1Df",
          "OwPmd0SSooV2HQx5Ua3clfRhnp8"
        ],
        "page": {
          "elements": [
            {
              "text_run": {
                "content": "test",
                "text_element_style": {
                  "bold": false,
                  "inline_code": false,
                  "italic": false,
                  "strikethrough": false,
                  "underline": false
                }
              }
            }
          ],
          "style": {
            "align": 1
          }
        },
        "parent_id": ""
      },