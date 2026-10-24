from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import ToolCall

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="I am user123, I would like a refund for the book and the pen",
            expected_output="A refund ticket for 30$ has been issued successfully",
            expected_tools=[
                ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user123"}),
                ToolCall(name="get_today_date",
                                         input_parameters={}),
                ToolCall(name="calculate_right_refund",
                         input_parameters={"user":"user123","items":[{"name":"book"},{"name":"pen"}]}),
                ToolCall(name="issue_refund_ticket",
                         input_parameters={"user":"user123", "refund_amount": 30}),
                
            ]
        ),
        Golden(
            input="I am user123, I would like a refund for the book",
            expected_output="A refund ticket for 23$ has been issued successfully",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user123"}),
                ToolCall(name="get_today_date",
                                         input_parameters={}),
                ToolCall(name="calculate_right_refund",
                         input_parameters={"user":"user123","items":[{"name":"book"}]}),
                ToolCall(name="issue_refund_ticket",
                         input_parameters={"user":"user123", "refund_amount": 23}),
                
            ]
        ),
        Golden(
            input="I am user123, I would like no refund, I just want to know what I purchased",
            expected_output="no refund tickets were issued only a list of what they bought",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user123"}),
            ]
        ),
        Golden(
            input="I am user999, I would like a refund for the book",
            expected_output="tell the user that the username is not valid and ask for username again before giving info about a refund",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user999"}),
            ]
        ),
        Golden(
            input="I am user126, I would like a refund for the water_bottle",
            expected_output="no refund given because it is outside of the 30 days guideline",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user126"}),
                ToolCall(name="get_today_date",
                         input_parameters={})
            ]
        ),
        Golden(
            input="I am user126, I would like a refund for the backpack and water_bottle",
            expected_output="A refund ticket for 45$ has been issued successfully only for the backpack. the water_bottle is not eligible for a refund because it is outside 30 days refund policy",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user126"}),
                ToolCall(name="get_today_date",
                         input_parameters={}),
                ToolCall(name="calculate_right_refund",
                         input_parameters={"user":"user126","items":[{"name":"backpack"}]}),
                ToolCall(name="issue_refund_ticket",
                         input_parameters={"user":"user126", "refund_amount": 45}),

            ]
        ),
        Golden(
            input="I am user126, I would like a refund for the sneakers",
            expected_output="no refund was given because you didn't purchase this item",
            expected_tools=[
               ToolCall(name="get_user_purchase_history",
                         input_parameters={"user":"user126"}),
            ]
        ),
    ]

)