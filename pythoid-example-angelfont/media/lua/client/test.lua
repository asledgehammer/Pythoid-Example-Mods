Events.OnKeyPressed.Add(function(key)
    if key == Keyboard.KEY_T then
        local uis = UIManager.getUI()
        for i = 1, uis:size() do
            local ui = uis:get(i - 1)
            print(ui)
            -- if ui.isMouseOver then
            --     print('ok')
            -- end
            debugPrint(ui)
            print(ui:isMouseOver())
        end
    end
end)
print('###################################3333');